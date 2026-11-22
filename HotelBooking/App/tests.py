from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile
from .exceptions import (HotelBookingError, InvalidContactError, InvalidGuestNameError,
                         InvalidPackError, InvalidPackQuantityError, InvalidStayDurationError)
from .guest import Guest
from .packs import Pack, PackCatalog, PerGroupPack, PerMorningPack, PerPersonPack

class AuthenticationTestCase(TestCase):

    def test_signup_creates_user_and_profile(self):
        """Test that submitting the signup form creates a User and a UserProfile."""
        signup_url = reverse('signup')  # Matches path name in urls.py
        
        # Simulate form data submission
        form_data = {
            'username': 'charlotte',
            'fullname': 'Charlotte Hamilton',
            'email': 'charlotte@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }
        
        response = self.client.post(signup_url, form_data)
        
        # Django redirects on successful form submission (status code 302)
        self.assertEqual(response.status_code, 302)
        
        # Verify the Django User was created in SQLite
        self.assertTrue(User.objects.filter(username='charlotte').exists())
        
        # Verify the UserProfile was created and linked correctly via OneToOneField
        user = User.objects.get(username='charlotte')
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.fullname, 'Charlotte Hamilton')
        self.assertEqual(profile.email, 'charlotte@example.com')

    def test_login_success(self):
        """Test that a registered user can log in successfully."""
        # 1. Pre-create a test user in the database
        user = User.objects.create_user(username='charlotte', password='SecurePass123!')
        
        login_url = reverse('login')
        
        # 2. Simulate posting credentials to login view
        credentials = {
            'username': 'charlotte',
            'password': 'SecurePass123!'
        }
        response = self.client.post(login_url, credentials)
        
        # 3. Successful login redirects the user (status code 302)
        self.assertEqual(response.status_code, 302)
        
        # 4. Verify the client session now flags the user as authenticated
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_failure_wrong_password(self):
        """Test that login fails with incorrect credentials and stays on the login page."""
        User.objects.create_user(username='charlotte', password='SecurePass123!')
        
        login_url = reverse('login')
        credentials = {
            'username': 'charlotte',
            'password': 'WrongPassword!'
        }
        response = self.client.post(login_url, credentials)
        
        # Should NOT redirect (status 200 means it re-rendered the form with errors)
        self.assertEqual(response.status_code, 200)
        
        # Verify user is NOT authenticated in the session
        self.assertFalse('_auth_user_id' in self.client.session)

# Guest Model Validation Tests
class GuestTests(SimpleTestCase):

    # Name whitespace formatting
    def test_valid_name_is_cleaned(self):
        self.assertEqual(Guest("    Spongebob   Squarepants ").name, "Spongebob Squarepants")

    # Empty name rejection
    def test_empty_name_is_rejected(self):
        with self.assertRaises(InvalidGuestNameError) as ctx:
            Guest("   ")
        self.assertEqual(str(ctx.exception), "Please enter a valid guest name.")

    # Block guest names with digits
    def test_name_with_numbers_is_rejected(self):
        with self.assertRaises(InvalidGuestNameError):
            Guest("R2D2")

    # Reject malformed email updates while keeping the previous valid email.
    def test_bad_email_is_rejected_and_old_email_is_kept(self):
        guest = Guest("Ana", email="ana@example.com")
        with self.assertRaises(InvalidContactError):
            guest.email = "not-an-email"
        self.assertEqual(guest.email, "ana@example.com")

# Itinerary Pack & Catalog Tests
class PackTests(SimpleTestCase):

    # Initialize a fresh PackCatalog instance before each test
    def setUp(self):
        self.catalog = PackCatalog()

    # verify per-person, per-morning, and per-group pricing rules
    def test_same_call_gives_different_results(self):
        spa = self.catalog.get("thermal-spa")
        breakfast = self.catalog.get("grand-breakfast")
        karaoke = self.catalog.get("karaoke-pod") 
        self.assertEqual(spa.calculate_cost(2, 3), 10400)
        self.assertEqual(breakfast.calculate_cost(2, 3), 9000)
        self.assertEqual(karaoke.calculate_cost(7, 3), 4400)  

    # confirm all specialized pack types inherit from the base Pack class
    def test_child_classes_inherit_from_pack(self):
        for child in (PerPersonPack, PerMorningPack, PerGroupPack):
            self.assertTrue(issubclass(child, Pack))

    # Reject zero or invalid quantities and stay durations
    def test_invalid_people_and_nights(self):
        pack = self.catalog.get("canopy-expedition")
        with self.assertRaises(InvalidPackQuantityError):
            pack.calculate_cost(0, 1)
        with self.assertRaises(InvalidStayDurationError):
            pack.calculate_cost(1, 0)

    # Filter packs by valid category and raise error on unknown categories
    def test_filter_by_category(self):
        self.assertEqual(len(self.catalog.by_category("adventure")), 3)
        self.assertEqual(len(self.catalog.by_category("all")), 9)
        with self.assertRaises(InvalidPackError):
            self.catalog.by_category("spa-day")

    # Full stay and Add-on total calculation
    def test_total_matches_the_design_proposal(self):
        # Deluxe room 4,800 x 3 nights + Canopy Expedition 4,500 x 2 people = 23,400
        lines, addons = self.catalog.price_selection({"canopy-expedition": 2}, nights=3)
        self.assertEqual(4800 * 3 + addons, 23400)

    # Ensure all custom domain exceptions inherit from HotelBookingError.
    def test_all_errors_share_one_parent(self):
        with self.assertRaises(HotelBookingError):
            self.catalog.get("nope")
