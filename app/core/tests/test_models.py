from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.test import TestCase

from ..models import User


class ModelTests(TestCase):

    def test_create_user_with_email_success(self):
        '''Test creating a new user using email is successful'''
        email = 'test@firozsoft.com'
        password = 'testpass123'
        user: AbstractBaseUser = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''Test the email for a new user is normalized'''
        email = 'test@FIROZSOFT.COM'
        user = get_user_model().objects.create_user(email=email)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        '''Test creating new user with no email raises error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        '''Test creating new superuser'''
        user: User = get_user_model().objects.create_superuser(
            'test@firozsoft.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
