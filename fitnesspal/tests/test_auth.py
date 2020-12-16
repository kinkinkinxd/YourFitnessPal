"""Authentication tests."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import reverse


class AuthenticationTest(TestCase):
    """Test cases for authentication system."""

    def setUp(self):
        """Initialize the user."""
        self.user = {
            'username': 'admin', 'password': 'easybing'
        }
        User.objects.create_user(**self.user)

    def test_user_logged_in(self):
        """Test if user can login and is authenticated in the website."""
        response = self.client.post(reverse('login'), {'username':'admin', 'password':'easybing'}, follow = True)  
        self.assertTrue(response.context['user'].is_authenticated)

    def test_user_enter_wrong_username(self):
        """Test that user is unauthenticated without logging in."""
        response = self.client.post(reverse('login'), {'username':'adme', 'password':'easybing'}, follow = True)  
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_user_enter_wrong_password(self):
        """Test that user is unauthenticated without logging in."""
        response = self.client.post(reverse('login'), {'username':'admin', 'password':'easybooong'}, follow = True)  
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_user_logged_out(self):
        """Test that when the user is logged out, it will redirect to home page."""
        response = self.client.post(reverse('login'), {'username':'admin', 'password':'easybing'}, follow = True)  
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_unauthenticated_user_redirect_to_login(self):
        """Test that when unauthenticated user try to access login required page, it will redirect to login page. """
        response = self.client.get(reverse('fitnesspal:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=%2Fprofile%2F')
