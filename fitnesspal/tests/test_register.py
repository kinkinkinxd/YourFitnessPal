"""Registration tests."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import reverse


class RegistrationTest(TestCase):
    """Test cases for registration system."""    

    def test_can_view_register_page(self):
        """Test if anyone can access the registration page and the correct template is used."""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '../templates/registration/signup.html')
    
    def test_user_register_successfully(self):
        """Test when the registration is completed, user will be redirected to home."""
        response = self.client.post(reverse('signup'), {
            'username': 'superman', 'first_name': 'super', 'last_name': 'man', 
            'email': 'superman@gmail.com','password1': 'verycoolpass', 'password2': 'verycoolpass'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_user_register_with_invalid_email(self):
        """Test that user can't register with invalid email."""
        response = self.client.post(reverse('signup'), {
            'username': 'superman', 'first_name': 'super', 'last_name': 'man', 
            'email': 'supermanhotmail','password1': 'super123', 'password2': 'super123'})
        self.assertEqual(response.status_code, 200)

    def test_user_registration_with_unmatching_password(self):
        """Test that user can't register with password that don't match."""
        response = self.client.post(reverse('signup'), {
            'username': 'superman', 'first_name': 'super', 'last_name': 'man', 
            'email': 'superman@gmail.com','password1': 'super123', 'password2': 'super123456'})
        self.assertEqual(response.status_code, 200)
    
    def test_register_with_existing_username(self):
        """If the username is already taken, the error message will be shown."""
        User.objects.create(username='superman', email='realsuperman@gmail.com', password='secret')
        response = self.client.post(reverse('signup'), {
            'username': 'superman', 'first_name': 'super', 'last_name': 'man', 
            'email': 'superman@gmail.com','password1': 'super123', 'password2': 'super123'})
        self.assertEqual(response.status_code, 200)