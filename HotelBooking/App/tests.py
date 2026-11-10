from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile

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