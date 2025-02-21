from django.contrib.auth.decorators import login_required
from django.utils.text import phone2numeric
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.contrib import messages
from urllib3 import request
from django.db import models
from django.contrib.auth import authenticate, login, logout
from .forms import ReviewForm, BookingForm
from .models import HotelRestro, FavoriteHotel, Review, Booking
from django.db.models import Q, Avg
from geopy.distance import geodesic
from django.shortcuts import redirect, render, get_object_or_404
from requests.exceptions import RequestException  # Import for handling specific request errors
from django.http import JsonResponse, HttpResponseRedirect
from rapidfuzz import fuzz, process
import requests

def home(request):
    return render(request, "hotels/home.html")

def about(request):
    return render(request, "hotels/about.html")

def services(request):
    return render(request, "hotels/services.html")

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(request, user)  # Log in the new user
        messages.success(request, "Registration successful! Redirected to home...")

        return redirect("home")

    return render(request, 'hotels/register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful! Redirecting to home...")

            return redirect("home")  # Redirect on successful login
        else:
            messages.error(request, "Username and password do not match.")
            return redirect("hotels/login")  # Redirect instead of render

    return render(request, "hotels/login.html")  # Render for GET requests

def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

def search_hotels(request):
    if request.method == "GET":
        user_lat = request.GET.get("lat")
        user_lon = request.GET.get("lon")
        request.session["user_lat"] = user_lat
        request.session["user_lon"] = user_lon
        query = request.GET.get("q", "").strip()

        if not user_lat or not user_lon:
            return JsonResponse({"error": "Location data is required."}, status=400)

        try:
            GEOAPIFY_API_KEY = "d9e349a2a2b84f88911d53456bd0ddce"
            GEOAPIFY_API_URL = "https://api.geoapify.com/v2/places"
            initial_radius = 5000
            max_radius = 20000
            step = 5000

            all_hotels = {}  # Use a dictionary to store unique hotels
            matching_hotels = []
            radius = initial_radius

            # Fetch hotels from the local database
            user_location = (float(user_lat), float(user_lon))
            db_hotels = HotelRestro.objects.all()
            local_hotels = [
                {
                    "name": hotel.name,
                    "address": hotel.address,
                    "latitude": hotel.latitude,
                    "longitude": hotel.longitude,
                    "phone": hotel.phone,
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
                    "apiKey": GEOAPIFY_API_KEY,
                }

                response = requests.get(GEOAPIFY_API_URL, params=params)
                response.raise_for_status()
                response_data = response.json()

                api_hotels = [
                    {
                        "name": feature["properties"].get("name", "Unnamed Hotel"),
                        "address": feature["properties"].get("formatted", "No address available"),
                        "latitude": feature["properties"]["lat"],
                        "longitude": feature["properties"]["lon"],
                        "phone": feature["properties"]
                        .get("contact", {})
                        .get("phone", "No phone available"),
                    }
                    for feature in response_data.get("features", [])
                ]

                # Add API hotels to all_hotels dictionary
                for hotel in api_hotels:
                    unique_key = (hotel["name"], hotel["latitude"], hotel["longitude"])
                    if unique_key not in all_hotels:
                        all_hotels[unique_key] = hotel

                # Stop increasing the radius if at least 5 unique hotels are found
                if len(all_hotels) >= 5:
                    break

                radius += step

            # Add local hotels to all_hotels dictionary
            for hotel in local_hotels:
                unique_key = (hotel["name"], hotel["latitude"], hotel["longitude"])
                if unique_key not in all_hotels:
                    all_hotels[unique_key] = hotel

            # Convert all_hotels back to a list for display
            all_hotels_list = list(all_hotels.values())

            # Apply fuzzy matching if a query is provided
            if query:
                matching_hotels = [
                    all_hotels_list[idx]
                    for _, score, idx in process.extract(
                        query,
                        [hotel["name"] for hotel in all_hotels_list],
                        scorer=fuzz.partial_ratio,
                        score_cutoff=70,
                    )
                ]

            # Determine which hotels to display
            hotels_to_display = matching_hotels if matching_hotels else all_hotels_list

            return render(
                request,
                "hotels/search_hotels.html",
                {
                    "hotels": hotels_to_display,
                    "query": query,
                    "exact_matches": bool(matching_hotels),
                    "fallback": not bool(matching_hotels),
                    "no_results": not hotels_to_display,
                    "radius_used": radius,  # Pass the radius used for the search
                },
            )

        except RequestException as e:
            print(f"Geoapify API Error: {e}")
            return render(
                request,
                "hotels/search_hotels.html",
                {
                    "hotels": [],
                    "query": query,
                    "exact_matches": False,
                    "fallback": False,
                    "no_results": True,
                    "error_message": "Could not fetch data from the Geoapify API. Please try again later.",
                },
            )

    return JsonResponse({"error": "Invalid request method."}, status=400)


@login_required
def hotel_details(request, lat, lon, name, *args, **kwargs):
    user_lat = request.session.get("user_lat")
    user_lon = request.session.get("user_lon")
    phone = request.GET.get("phone")
    address = request.GET.get("address", "Not provided")
    rating_range = range(1,6)

    # Check if hotel exists, otherwise create it
    hotel, created = HotelRestro.objects.get_or_create(
        name=name, latitude=lat, longitude=lon,
        defaults={"address": address, "phone": phone}
    )

    reviews = Review.objects.filter(hotel=hotel)
    average_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or "No ratings yet"

    # Check if the hotel is a favorite for the current user
    is_favorite = FavoriteHotel.objects.filter(
        user=request.user, name=name, latitude=lat, longitude=lon
    ).exists()

    # Handle POST request for submitting a review
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            review_text = form.cleaned_data['review_text']
            review = Review(
                user=request.user,
                hotel=hotel,
                rating=rating,
                review_text=review_text,
            )
            review.save()
            messages.success(request, "Your review has been submitted!")
            return redirect("hotel_details", lat=lat, lon=lon, name=name)
    else:
        form = ReviewForm()

    # Pass the initial rating value for the form
    return render(
        request,
        "hotels/hotel_details.html",
        {
            "latitude": lat,
            "longitude": lon,
            "name": name,
            "user_lat": user_lat,
            "user_lon": user_lon,
            "address": address,
            "phone": phone,
            "is_favorite": is_favorite,
            "reviews": reviews,
            "average_rating": average_rating,
            "form": form,
            "rating_range":rating_range,
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

        # Toggle favorite status
        favorite, created = FavoriteHotel.objects.get_or_create(
            user=request.user,
            name=name,
            latitude=latitude,
            longitude=longitude,
            defaults={"address": address, "phone": phone},
        )
        if not created:  # If already exists, remove it
            favorite.delete()

        # Redirect back to the hotel details page with user location and other info
        query_params = urlencode({
            "user_lat": user_lat,
            "user_lon": user_lon,
            "address": address,
            "phone": phone,
        })
        redirect_url = f"{reverse('hotel_details', args=[latitude, longitude, name])}?{query_params}"
        return HttpResponseRedirect(redirect_url)

    return JsonResponse({"error": "Invalid request method."}, status=400)


@login_required
def favorites_list(request):
    favorites = FavoriteHotel.objects.filter(user=request.user)
    user_lat = request.session.get("user_lat")
    phone = request.GET.get("phone")
    user_lon = request.session.get("user_lon")

    # Add average rating for each favorite hotel
    for favorite in favorites:
        hotel = HotelRestro.objects.get(name=favorite.name, latitude=favorite.latitude, longitude=favorite.longitude)
        reviews = Review.objects.filter(hotel=hotel)
        favorite.average_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0

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
    # Get the favorite hotel entry
    favorite = get_object_or_404(FavoriteHotel, id=favorite_id, user=request.user)
    # Delete the entry
    favorite.delete()
    # Redirect back to the favorites list
    return redirect("favorites_list")

def error_page(request):
    return render(request, "hotels/error_page.html", {"message": "Hotel not found."})

@login_required
def book_hotel(request, hotel_name, lat, lon):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.hotel_name = hotel_name
            booking.lat = lat
            booking.lon = lon
            booking.user = request.user
            booking.save()
            return redirect('booking_success')  # Redirect to success page
    else:
        form = BookingForm()

    # Render the same hotel details page with form errors
    return render(request, 'hotels/hotel_details.html', {
        'form': form,
        'name': hotel_name  # Ensure 'name' matches the URL parameter
    })

def booking_success(request):
    return render(request, 'hotels/booking_success.html')

def my_bookings(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)
    else:
        bookings = []  # If not logged in, show no bookings

    return render(request, 'hotels/my_bookings.html', {'bookings': bookings})

def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('my_bookings')