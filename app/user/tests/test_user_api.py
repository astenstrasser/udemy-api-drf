from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient 
from rest_framework import status


CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_should_be_successful_when_creating_an_user_with_valid_payload(self):
        payload = {'email' : 'example@example.com',
                   'password': 'password',
                   'name': 'User Name'}
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)


    def test_should_not_create_an_user_when_user_already_exists(self):
        payload = {'email' : 'example@example.com',
                   'password': 'password',
                   'name': 'User Name'}
        create_user(**payload)                   
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_password_should_be_longer_than_5_chars(self):
        payload = {'email' : 'example@example.com',
                   'password': 'pas',
                   'name': 'User Name'}
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email = payload['email']).exists()
        self.assertFalse(user_exists)
