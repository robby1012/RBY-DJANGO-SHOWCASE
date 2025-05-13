from django.test import TestCase
from django.urls import reverse


class AuthorizationTests(TestCase):
    fixtures = ['fixtures/superuser.yaml', ]
    payload  = {
        'username': 'sudo',
        'password': 'sudo987!@#'
    }

    def testSuccess(self):
        # Attempt to sign by token from username and password
        post = self.client.post(
            reverse('authentication.token'),
            data={
                'username': self.payload['username'],
                'password': self.payload['password']
            }
        )
        self.assertEqual(post.status_code, 200)

    def testFailed(self):
        # Attempt to sign by token from username and password
        post = self.client.post(
            reverse('authentication.token'),
            data={
                'username': 'notmyusername',
                'password': 'notmypassword'
            }
        )

        self.assertNotEqual(post.status_code, 200)


class RegistrationTests(TestCase):
    payload = {
        'first_name': 'jane',
        'last_name': 'doe',
        'username': 'jane_doe',
        'email': 'jane_doe@mail.com',
        'password': 'mypassword12345',
        'password2': 'mypassword12345'
    }

    def testSuccess(self):
        # Attempt to register
        post = self.client.post(
            '/api/v1/authentication/registration/',
            data=self.payload
        )
        response = post.json()
        self.assertEqual(post.status_code, 201)
        self.assertEqual(response.get('email'), 'jane_doe@mail.com')

        # Attempt to sign by token from username and password
        post = self.client.post(
            reverse('authentication.token'),
            data={
                'username': self.payload['username'],
                'password': self.payload['password']
            }
        )
        self.assertEqual(post.status_code, 200)

    def testFailed(self):
        payload = {
            'first_name': 'jane',
            'last_name': 'doe',
            'username': 'jane_doe',
            'email': 'jane_doe@mail.com',
            'password': 'mypassword12345',
            'password2': 'mypassword54321'
        }

        # Attempt to register with mismatch password
        post = self.client.post(
            '/api/v1/authentication/registration/',
            data=payload
        )

        self.assertNotEqual(post.status_code, 201)
