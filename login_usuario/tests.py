from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework import status


class TestLoginUser(TestCase):

    def test_create_user_admin(self):
        email = "cesar@gmail.com"
        password = "cesar123"

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_email_normalized(self):
        email = 'cesar@GMAIL.com'
        password = 'cesar123'

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(email.lower(), user.email)

    def test_invalid_email(self):
        email = None
        password = 'cesar123'

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=email, password=password)

    def test_superuser_created(self):
        email = "cesar@gmail.com"
        password = 'cesar1233'

        user = get_user_model().objects.create_superuser(email=email, password=password)

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_login_super_user(self):
        payload = {
            'email': 'cesar123@gmail.com',
            'password': 'cesar123',
            'name': 'cesar',
        }

        cli = Client()
        get_user_model().objects.create_superuser(**payload)
        url = "/auth/jwt/create/"
        configs = {
            'HTTP_ACCEPT': 'application/json',
            'content_type': 'application/json',
        }
        response = cli.post(url, payload, **configs)

        self.assertEqual(status.HTTP_200_OK, response.status_code)



