from django.test import TestCase
from django.contrib.auth.models import User
from .models import MenuItem, Booking
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class MenuItemTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item = MenuItem.objects.create(
            title="Pizza",
            price=9.99,
            inventory=10
        )

    def test_menu_item_title(self):
        self.assertEqual(self.item.title, "Pizza")

    def test_menu_item_price(self):
        self.assertEqual(float(self.item.price), 9.99)

    def test_menu_item_inventory(self):
        self.assertEqual(self.item.inventory, 10)

    def test_menu_item_str(self):
        self.assertEqual(str(self.item), "Pizza")


class BookingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.booking = Booking.objects.create(
            name="John Doe",
            no_of_guests=4,
            bookingDate=timezone.now()
        )

    def test_booking_name(self):
        self.assertEqual(self.booking.name, "John Doe")

    def test_booking_guests(self):
        self.assertEqual(self.booking.no_of_guests, 4)

    def test_booking_str(self):
        self.assertEqual(str(self.booking), "John Doe")


class MenuAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        MenuItem.objects.create(title="Pasta", price=12.99, inventory=5)

    def test_get_menu_items(self):
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, 200)

    def test_post_menu_item(self):
        data = {'title': 'Salad', 'price': 7.99, 'inventory': 20}
        response = self.client.post('/api/menu/', data)
        self.assertEqual(response.status_code, 201)


class BookingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_bookings(self):
        response = self.client.get('/api/tables/')
        self.assertEqual(response.status_code, 200)

    def test_post_booking(self):
        data = {
            'name': 'Jane Doe',
            'no_of_guests': 2,
            'bookingDate': timezone.now()
        }
        response = self.client.post('/api/tables/', data)
        self.assertEqual(response.status_code, 201)
