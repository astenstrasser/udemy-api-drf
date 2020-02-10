from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'MyPass!'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'example@EXAMPLE.com'
        user = get_user_model().objects.create_user(email, 'testPass123')

        self.assertEqual(user.email, email.lower())

    def test_when_new_user_is_created_email_should_be_validated(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'password123')
