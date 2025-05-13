import uuid

from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class BookTests(TestCase):
    fixtures = ('fixtures/superuser.yaml', 'fixtures/libraries.yaml')

    def testSuccess(self):
        login_payload = {
            'username': 'sudo',
            'password': 'sudo987!@#'
        }
        book_payload = {
            'title'   : 'Lorem ipsum dolor sit amet',
            'synopsis': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
            'author'  : 'John doe',
            'publish' : 2024,
            'price'   : 100000,
            'copies'  : 1
        }

        # attempt to lists as a guest (unauthorized)
        req = self.client.get(
            reverse('library.book-list')
        )

        self.assertEqual(req.status_code, 200)

        # Attempt to sign by token from username and password
        post = self.client.post(
            reverse('authentication.token'),
            data = login_payload
        )

        response = post.json()
        token = response.get('token')
        self.assertEqual(post.status_code, 200)

        # Attempt to create a book
        headers = {
            'Authorization': f'Token {token}'
        }

        post = self.client.post(
            '/api/v1/library/book/',
            headers=headers,
            data=book_payload
        )
        response = post.json()
        self.assertEqual(post.status_code, 201)

        # Attempt to update a book that just been inserted
        book_payload['copies'] += 2
        book_payload['price']  -= 10000
        update = self.client.patch(
            f'/api/v1/library/book/{response.get("uuid")}/',
            headers=headers,
            data=book_payload,
            content_type='application/json'
        )
        self.assertEqual(update.status_code, 200)

        # Attempt to delete a book that just been modified
        delete = self.client.delete(
            f'/api/v1/library/book/{response.get("uuid")}/',
            headers=headers
        )
        self.assertEqual(delete.status_code, 204)

    def testFailed(self):
        login_payload = {
            'username': 'sudo',
            'password': 'sudo987!@#'
        }
        book_payload = {
            'title'   : 'Lorem ipsum dolor sit amet',
            'synopsis': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
            'author'  : 'John doe',
            'publish' : 2024,
            'price'   : 100000,
            'copies'  : 1
        }

        # Attempt to insert without token
        post = self.client.post(
            '/api/v1/library/book/',
            data=book_payload
        )
        self.assertEqual(post.status_code, 401)

        # Attempt to sign by token from username and password
        post = self.client.post(
            reverse('authentication.token'),
            data = login_payload
        )

        response = post.json()
        token = response.get('token')
        self.assertEqual(post.status_code, 200)

        headers = {
            'Authorization': f'Token {token}'
        }

        # Attempt to update without valid uuid
        update = self.client.patch(
            f'/api/v1/library/book/invalid_uuid/',
            headers=headers,
            data=book_payload,
            content_type='application/json'
        )
        self.assertEqual(update.status_code, 404)

        # Attempt to delete without valid uuid
        delete = self.client.delete(
            f'/api/v1/library/book/invalid_uuid/',
            headers=headers
        )
        self.assertEqual(delete.status_code, 404)


class InquiryTests(TestCase):
    fixtures = ('fixtures/superuser.yaml', 'fixtures/libraries.yaml')

    def testSuccess(self):
        login_payload = {
            'username': 'sudo',
            'password': 'sudo987!@#'
        }

        # Get all the books
        req = self.client.get(
            reverse('library.book-list')
        )
        books = req.json()['results']
        self.assertEqual(req.status_code, 200)

        # Attempt to sign by token from username and password
        post = self.client.post(
            reverse('authentication.token'),
            data = login_payload
        )

        response = post.json()
        token = response.get('token')
        self.assertEqual(post.status_code, 200)

        headers = {
            'Authorization': f'Token {token}'
        }

        # attempt to inquiry the first book
        post = self.client.post(
            '/api/v1/library/inquiry/',
            headers=headers,
            data={
                'uuid': books[0]['uuid'], 'copies': 1
            }
        )
        self.assertEqual(post.status_code, 201)

        # attempt to inquiry the second book
        post = self.client.post(
            '/api/v1/library/inquiry/',
            headers=headers,
            data={
                'uuid': books[1]['uuid'], 'copies': 3
            }
        )
        data = post.json()
        self.assertEqual(post.status_code, 201)

        # attempt to update inquiry on the second book
        post = self.client.patch(
            f'/api/v1/library/inquiry/{data["uuid"]}/',
            headers=headers,
            data={
                'copies': 4
            },
            content_type='application/json'
        )
        self.assertEqual(post.status_code, 200)

    def testFailed(self):
        login_payload = {
            'username': 'sudo',
            'password': 'sudo987!@#'
        }

        # Get all the books
        req = self.client.get(
            reverse('library.book-list')
        )
        books = req.json()['results']
        self.assertEqual(req.status_code, 200)

        # Attempt to sign by token from username and password
        post = self.client.post(
            reverse('authentication.token'),
            data = login_payload
        )

        response = post.json()
        token = response.get('token')
        self.assertEqual(post.status_code, 200)

        headers = {
            'Authorization': f'Token {token}'
        }

        # attempt to inquiry the first book with exceeding copies
        post = self.client.post(
            '/api/v1/library/inquiry/',
            headers=headers,
            data={
                'uuid': books[0]['uuid'], 'copies': 10
            }
        )
        self.assertEqual(post.status_code, 400)

        # attempt to inquiry the second book with uuid not valid
        post = self.client.post(
            '/api/v1/library/inquiry/',
            headers=headers,
            data={
                'uuid': uuid.uuid4(), 'copies': 3
            }
        )
        self.assertEqual(post.status_code, 404)


class LendingOrReturnTests(TestCase):
    fixtures = ('fixtures/superuser.yaml', 'fixtures/libraries.yaml')

    def testSuccess(self):
        login_payload = {
            'username': 'sudo',
            'password': 'sudo987!@#'
        }

        # Get all the books
        req = self.client.get(
            reverse('library.book-list')
        )
        books = req.json()['results']
        self.assertEqual(req.status_code, 200)

        # Attempt to sign by token from username and password
        post = self.client.post(
            reverse('authentication.token'),
            data = login_payload
        )

        response = post.json()
        token = response.get('token')
        self.assertEqual(post.status_code, 200)

        headers = {
            'Authorization': f'Token {token}'
        }

        post = self.client.post(
            '/api/v1/library/inquiry/',
            headers=headers,
            data={
                'uuid': books[0]['uuid'], 'copies': 1
            }
        )
        inquiries = post.json()
        self.assertEqual(post.status_code, 201)

        # attempt to update status to leased for the first book
        post = self.client.patch(
            f'/api/v1/library/lending_or_return/{inquiries["uuid"]}/',
            headers=headers,
            data={'is_cancel': False},
            content_type='application/json'
        )
        self.assertEqual(post.status_code, 200)

        # attempt to update status to return for the first book
        post = self.client.patch(
            f'/api/v1/library/lending_or_return/{inquiries["uuid"]}/',
            headers=headers,
            data={'is_cancel': False},
            content_type='application/json'
        )
        self.assertEqual(post.status_code, 200)
