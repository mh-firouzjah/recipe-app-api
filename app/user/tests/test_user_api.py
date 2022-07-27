from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    '''Helper function to create user object for testing perposes'''
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    '''Test the user API (public)'''

    def setUp(self):
        self.client = APIClient()
        return super().setUp()

    def test_create_user_success(self):
        '''Test creating user with valid payload is successful'''
        payload = {
            'email': 'test@firozsoft.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))

        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        '''Test creation of user that already exists fails'''
        payload = {'email': 'test@firozsoft.com', 'password': 'testpass'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_to_short(self):
        '''Test that the password must be more than 5 characters'''
        payload = {'email': 'test@firozsoft.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_generat_token_for_user(self):
        '''Test that a token is generated for the user'''
        payload = {'email': 'test@firozsoft.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_generate_token_invalid_credentials(self):
        '''Test that token is not generated in case of invalid credentials'''
        create_user(email='test@firozsoft.com', password='testpass')
        payload = {'email': 'test@firozsoft.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_token_no_user(self):
        '''Test that token is not generated if user doesn't exists'''
        payload = {'email': 'test@firozsoft.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_token_missing_field(self):
        '''Test that email and password are required'''
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
