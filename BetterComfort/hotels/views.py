import os
from urllib.parse import urlencode
import requests
from requests.exceptions import RequestException
from geopy.distance import geodesic
from rapidfuzz import fuzz, process

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BookingForm, ReviewForm
from .models import Booking, FavoriteHotel, HotelRestro, Review


def home(request):
    return render(request, "hotels/home.html")


def about(request):
    return render(request, "hotels/about.html")


def services(request):
    return render(request, "hotels/services.html")


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        # Create user safely
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, "Registration successful! Welcome to BetterComfort.")
        return redirect("home")

    return render(request, 'hotels/register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "hotels/login.html")


def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


def search_hotels(request):
    if request.method == "GET":
        user_lat = request.GET.get("lat")
        user_lon = request.GET.get("lon")
        query = request.GET.get("q", "").strip()

        if not user_lat or not user_lon:
            return JsonResponse({"error": "Location coordinates (lat, lon) are required."}, status=400)

        request.session["user_lat"] = user_lat
        request.session["user_lon"] = user_lon

        try:
            geoapify_key = getattr(settings, 'GEOAPIFY_API_KEY', 'd9e349a2a2b84f88911d53456bd0ddce')
            geoapify_url = "https://api.geoapify.com/v2/places"
            initial_radius = 5000
            max_radius = 20000
            step = 5000

            all_hotels = {}
            matching_hotels = []
            radius = initial_radius

            # Fetch hotels from the local database within max radius
            user_location = (float(user_lat), float(user_lon))
            db_hotels = HotelRestro.objects.all()
            local_hotels = [
                {
                    "name": hotel.name,
                    "address": hotel.address,
                    "latitude": hotel.latitude,
                    "longitude": hotel.longitude,
                    "phone": hotel.phone or "Not provided",
                }
                for hotel in db_hotels
                if geodesic((hotel.latitude, hotel.longitude), user_location).meters <= max_radius
            ]

            # Fetch hotels within increasing radius from Geoapify API
            while radius <= max_radius:
                params = {
                    "categories": "accommodation.hotel,catering.restaurant",
                    "filter": f"circle:{user_lon},{user_lat},{radius}",
                    "bias": f"proximity:{user_lon},{user_lat}",
                    "limit": 100,
                    "apiKey": geoapify_key,
                }

                try:
                    response = requests.get(geoapify_url, params=params, timeout=8)
                    if response.status_code == 200:
                        response_data = response.json()
                        api_hotels = [
                            {
                                "name": feature["properties"].get("name", "Unnamed Hotel"),
                                "address": feature["properties"].get("formatted", "No address available"),
                                "latitude": feature["properties"]["lat"],
                                "longitude": feature["properties"]["lon"],
                                "phone": feature["properties"].get("contact", {}).get("phone", "No phone available"),
                            }
                            for feature in response_data.get("features", [])
                            if feature.get("properties", {}).get("name")
                        ]

                        for hotel in api_hotels:
                            unique_key = (hotel["name"], round(hotel["latitude"], 4), round(hotel["longitude"], 4))
                            if unique_key not in all_hotels:
                                all_hotels[unique_key] = hotel

                        if len(all_hotels) >= 5:
                            break
                except RequestException as api_err:
                    print(f"Geoapify request error: {api_err}")
                    break

                radius += step

            # Add local database hotels to pool
            for hotel in local_hotels:
                unique_key = (hotel["name"], round(hotel["latitude"], 4), round(hotel["longitude"], 4))
                if unique_key not in all_hotels:
                    all_hotels[unique_key] = hotel

            all_hotels_list = list(all_hotels.values())

            # Apply fuzzy matching if a search query is provided
            if query and all_hotels_list:
                hotel_names = [h["name"] for h in all_hotels_list]
                extracted = process.extract(
                    query,
                    hotel_names,
                    scorer=fuzz.partial_ratio,
                    score_cutoff=65,
                )
                matching_hotels = [all_hotels_list[idx] for _, score, idx in extracted]

            hotels_to_display = matching_hotels if query and matching_hotels else all_hotels_list

            return render(
                request,
                "hotels/search_hotels.html",
                {
                    "hotels": hotels_to_display,
                    "query": query,
                    "exact_matches": bool(query and matching_hotels),
                    "fallback": bool(query and not matching_hotels and all_hotels_list),
                    "no_results": not bool(hotels_to_display),
                    "radius_used": radius if radius <= max_radius else max_radius,
                },
            )

        except Exception as e:
            print(f"Hotel search unexpected error: {e}")
            return render(
                request,
                "hotels/search_hotels.html",
                {
                    "hotels": [],
                    "query": query,
                    "exact_matches": False,
                    "fallback": False,
                    "no_results": True,
                    "error_message": "Could not fetch nearby hotel data at this moment. Please try again.",
                },
            )

    return JsonResponse({"error": "Invalid request method."}, status=400)


@login_required
def hotel_details(request, lat, lon, name, *args, **kwargs):
    user_lat = request.session.get("user_lat")
    user_lon = request.session.get("user_lon")
    phone = request.GET.get("phone")
    address = request.GET.get("address", "Not provided")
    rating_range = range(1, 6)

    try:
        lat_val = float(lat)
        lon_val = float(lon)
    except (ValueError, TypeError):
        return redirect("error_page")

    # Check if hotel exists in local DB, otherwise create record
    hotel, _ = HotelRestro.objects.get_or_create(
        name=name,
        latitude=lat_val,
        longitude=lon_val,
        defaults={"address": address, "phone": phone}
    )

    reviews = Review.objects.filter(hotel=hotel).order_by('-created_at')
    avg_calc = reviews.aggregate(Avg("rating"))["rating__avg"]
    average_rating = round(avg_calc, 1) if avg_calc else "No ratings yet"

    is_favorite = FavoriteHotel.objects.filter(
        user=request.user, name=name, latitude=lat_val, longitude=lon_val
    ).exists()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.hotel = hotel
            review.save()
            messages.success(request, "Your review has been submitted!")
            return redirect("hotel_details", lat=lat_val, lon=lon_val, name=name)
    else:
        form = ReviewForm()

    return render(
        request,
        "hotels/hotel_details.html",
        {
            "latitude": lat_val,
            "longitude": lon_val,
            "name": name,
            "user_lat": user_lat,
            "user_lon": user_lon,
            "address": address,
            "phone": phone,
            "is_favorite": is_favorite,
            "reviews": reviews,
            "average_rating": average_rating,
            "form": form,
            "rating_range": rating_range,
        },
    )


@login_required
def save_favorite(request):
    if request.method == "POST":
        name = request.POST.get("name")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        user_lat = request.session.get("user_lat", "")
        user_lon = request.session.get("user_lon", "")
        address = request.POST.get("address", "")
        phone = request.POST.get("phone")

        if not name or not latitude or not longitude:
            return JsonResponse({"error": "Missing hotel parameters."}, status=400)

        lat_val = float(latitude)
        lon_val = float(longitude)

        favorite, created = FavoriteHotel.objects.get_or_create(
            user=request.user,
            name=name,
            latitude=lat_val,
            longitude=lon_val,
            defaults={"address": address, "phone": phone},
        )
        if not created:
            favorite.delete()

        query_params = urlencode({
            "user_lat": user_lat,
            "user_lon": user_lon,
            "address": address,
            "phone": phone,
        })
        redirect_url = f"{reverse('hotel_details', args=[lat_val, lon_val, name])}?{query_params}"
        return HttpResponseRedirect(redirect_url)

    return JsonResponse({"error": "Invalid request method."}, status=400)


@login_required
def favorites_list(request):
    favorites = FavoriteHotel.objects.filter(user=request.user).order_by('-id')
    user_lat = request.session.get("user_lat")
    user_lon = request.session.get("user_lon")
    phone = request.GET.get("phone")

    for favorite in favorites:
        hotel = HotelRestro.objects.filter(
            name=favorite.name,
            latitude=favorite.latitude,
            longitude=favorite.longitude
        ).first()
        if hotel:
            reviews = Review.objects.filter(hotel=hotel)
            favorite.average_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0
        else:
            favorite.average_rating = 0

    return render(
        request,
        "hotels/favorites_list.html",
        {
            "favorites": favorites,
            "user_lat": user_lat,
            "user_lon": user_lon,
            "phone": phone,
        },
    )


@login_required
def delete_favorite(request, favorite_id):
    favorite = get_object_or_404(FavoriteHotel, id=favorite_id, user=request.user)
    favorite.delete()
    messages.success(request, "Favorite hotel removed.")
    return redirect("favorites_list")


def error_page(request):
    return render(request, "hotels/error_page.html", {"message": "Hotel not found."})


@login_required
def book_hotel(request, hotel_name, lat, lon):
    try:
        lat_val = float(lat)
        lon_val = float(lon)
    except (ValueError, TypeError):
        return redirect("error_page")

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.hotel_name = hotel_name
            booking.lat = lat_val
            booking.lon = lon_val
            booking.user = request.user
            booking.save()
            messages.success(request, f"Booking confirmed for {hotel_name}!")
            return redirect('booking_success')
    else:
        form = BookingForm()

    return render(request, 'hotels/hotel_details.html', {
        'form': form,
        'name': hotel_name,
        'latitude': lat_val,
        'longitude': lon_val,
    })


def booking_success(request):
    return render(request, 'hotels/booking_success.html')


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'hotels/my_bookings.html', {'bookings': bookings})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Booking cancelled successfully.")
    return redirect('my_bookings')