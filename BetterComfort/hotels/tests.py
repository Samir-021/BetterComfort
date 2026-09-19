import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import HotelRestro, FavoriteHotel, Review, Booking
from .converters import FloatConverter


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.hotel = HotelRestro.objects.create(
            name='Grand Himalayan Hotel',
            address='Kathmandu, Nepal',
            phone='+977-1-4444444',
            latitude=27.7172,
            longitude=85.3240
        )

    def test_hotel_creation_and_clean(self):
        self.assertEqual(str(self.hotel), 'Grand Himalayan Hotel')
        self.assertEqual(self.hotel.latitude, 27.7172)
        self.assertEqual(self.hotel.longitude, 85.3240)

        # Invalid latitude
        invalid_hotel = HotelRestro(
            name='Invalid Latitude Hotel',
            address='Nowhere',
            latitude=95.0,
            longitude=85.0
        )
        with self.assertRaises(ValidationError):
            invalid_hotel.clean()

        # Invalid longitude
        invalid_hotel_lon = HotelRestro(
            name='Invalid Longitude Hotel',
            address='Nowhere',
            latitude=25.0,
            longitude=190.0
        )
        with self.assertRaises(ValidationError):
            invalid_hotel_lon.clean()

    def test_hotel_average_rating(self):
        self.assertIsNone(self.hotel.get_average_rating())

        Review.objects.create(
            user=self.user,
            hotel=self.hotel,
            rating=5,
            review_text='Excellent service and view!'
        )
        Review.objects.create(
            user=self.user,
            hotel=self.hotel,
            rating=3,
            review_text='Decent stay.'
        )

        avg = self.hotel.get_average_rating()
        self.assertEqual(avg, 4.0)

    def test_favorite_hotel(self):
        fav = FavoriteHotel.objects.create(
            user=self.user,
            name=self.hotel.name,
            latitude=self.hotel.latitude,
            longitude=self.hotel.longitude,
            address=self.hotel.address,
            phone=self.hotel.phone
        )
        self.assertIn(self.hotel.name, str(fav))
        self.assertIn(self.user.username, str(fav))

    def test_booking_model(self):
        booking = Booking.objects.create(
            user=self.user,
            hotel_name=self.hotel.name,
            lat=self.hotel.latitude,
            lon=self.hotel.longitude,
            check_in=datetime.date.today(),
            check_out=datetime.date.today() + datetime.timedelta(days=2),
            adults=2,
            children=1
        )
        self.assertEqual(booking.adults, 2)
        self.assertEqual(booking.children, 1)
        self.assertIn(self.hotel.name, str(booking))


class ConverterTests(TestCase):
    def test_float_converter(self):
        converter = FloatConverter()
        self.assertEqual(converter.to_python('27.7172'), 27.7172)
        self.assertEqual(converter.to_python('-85.3240'), -85.3240)
        self.assertEqual(converter.to_url(27.7172), '27.7172')


class ViewAndAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='userone',
            email='userone@example.com',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='usertwo',
            email='usertwo@example.com',
            password='password123'
        )
        self.hotel = HotelRestro.objects.create(
            name='Yak and Yeti Comfort',
            address='Durbar Marg, Kathmandu',
            phone='+977-1-4248999',
            latitude=27.7110,
            longitude=85.3180
        )

    def test_public_pages_load(self):
        for route_name in ['home', 'about', 'services', 'login', 'register']:
            response = self.client.get(reverse(route_name))
            self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'safePassword123',
            'password2': 'safePassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_registration_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'mismatchuser',
            'email': 'mismatch@example.com',
            'password': 'password1',
            'password2': 'password2'
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='mismatchuser').exists())

    def test_login_and_logout(self):
        login_response = self.client.post(reverse('login'), {
            'username': 'userone',
            'password': 'password123'
        })
        self.assertEqual(login_response.status_code, 302)

        logout_response = self.client.get(reverse('logout'))
        self.assertEqual(logout_response.status_code, 302)

    def test_my_bookings_requires_login(self):
        # Anonymous user should redirect to login
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 302)

        # Authenticated user should see bookings
        self.client.login(username='userone', password='password123')
        Booking.objects.create(
            user=self.user1,
            hotel_name='Yak and Yeti Comfort',
            lat=27.7110,
            lon=85.3180,
            check_in=datetime.date.today(),
            check_out=datetime.date.today() + datetime.timedelta(days=1),
            adults=1,
            children=0
        )
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yak and Yeti Comfort')

    def test_delete_booking_security(self):
        booking_user1 = Booking.objects.create(
            user=self.user1,
            hotel_name='User1 Hotel',
            lat=27.7,
            lon=85.3,
            check_in=datetime.date.today(),
            check_out=datetime.date.today() + datetime.timedelta(days=1),
            adults=1,
            children=0
        )

        # User 2 logs in and attempts to delete User 1's booking
        self.client.login(username='usertwo', password='password123')
        delete_url = reverse('delete_booking', args=[booking_user1.id])
        response = self.client.get(delete_url)

        # Must return 404 (Not Found) because booking belongs to User 1
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Booking.objects.filter(id=booking_user1.id).exists())

        # User 1 logs in and deletes their own booking
        self.client.login(username='userone', password='password123')
        response_owner = self.client.get(delete_url)
        self.assertEqual(response_owner.status_code, 302)
        self.assertFalse(Booking.objects.filter(id=booking_user1.id).exists())

    def test_favorites_list_safe_lookup(self):
        self.client.login(username='userone', password='password123')
        # Create a favorite that has no matching HotelRestro in DB
        FavoriteHotel.objects.create(
            user=self.user1,
            name='Nonexistent Hotel in DB',
            latitude=28.0,
            longitude=84.0,
            address='Himalayas',
            phone='12345'
        )

        response = self.client.get(reverse('favorites_list'))
        # Must not raise 500 error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nonexistent Hotel in DB')

    def test_search_hotels_missing_coordinates(self):
        response = self.client.get(reverse('search_hotels'))
        self.assertEqual(response.status_code, 400)
