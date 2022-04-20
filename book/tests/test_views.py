import json
from datetime import datetime

from django.urls import reverse
from peewee import *
from rest_framework import status

from book.models import Author, Book, Publisher
from book.tests import BaseTestCase

MODELS = [Author, Book, Publisher, Book.authors.get_through_model()]


class GetAllBooksTest(BaseTestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(MODELS, methodName=methodName)

    def setUp(self):
        super().setUp()
        with self.test_db:
            self.publisher = Publisher.create(
                name="name",
                address="address",
                city="city",
                country="country",
                website="website",
            )
            Book.create(
                title="test book 1",
                description="test book 1 description",
                publication_date=datetime.now(),
                publisher=self.publisher,
            )
            Book.create(
                title="test book 2",
                description="test book 2 description",
                publication_date=datetime.now(),
                publisher=self.publisher,
            )

    def test_get_all_books(self):
        # get API response
        response = self.client.get(reverse("book:book_main"))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())


class GetSingleBookTest(BaseTestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(MODELS, methodName=methodName)

    def setUp(self):
        super().setUp()
        with self.test_db:
            self.publisher = Publisher.create(
                name="name",
                address="address",
                city="city",
                country="country",
                website="website",
            )
            self.book1 = Book.create(
                title="test book 1",
                description="test book 1 description",
                publication_date=datetime.now(),
                publisher=self.publisher,
            )
            self.book2 = Book.create(
                title="test book 2",
                description="test book 2 description",
                publication_date=datetime.now(),
                publisher=self.publisher,
            )

    def test_get_valid_single_book(self):
        response = self.client.get(
            reverse("book:book_detail", kwargs={"pk": self.book2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_book(self):
        response = self.client.get(reverse("book:book_detail", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewBookTest(BaseTestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(MODELS, methodName=methodName)

    def setUp(self):
        super().setUp()
        with self.test_db:
            self.publisher = Publisher.create(
                name="name",
                address="address",
                city="city",
                country="country",
                website="website",
            )
            self.authors = [
                Author.create(
                    first_name="first_name",
                    last_name="last_name",
                )
            ]
            self.book1 = Book.create(
                title="test book 1",
                description="test book 1 description",
                publication_date=datetime.now(),
                publisher=self.publisher,
            )
            self.book2 = Book.create(
                title="test book 2",
                description="test book 2 description",
                publication_date=datetime.now(),
                publisher=self.publisher,
            )

            self.valid_payload = {
                "title": "Book1",
                "description": "Book1 Description",
                "publication_date": "2022-04-15",
                "publisher_id": self.publisher.id,
                "authors_ids": [item.id for item in self.authors],
            }

            self.invalid_payload = {"title": "", "description": "Book2 Description"}

    def test_create_valid_book(self):
        response = self.client.post(
            reverse("book:book_main"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

    def test_create_invalid_book(self):
        response = self.client.post(
            reverse("book:book_main"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleBookTest(BaseTestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(MODELS, methodName=methodName)

    def setUp(self):
        super().setUp()
        with self.test_db:

            self.publisher = Publisher.create(
                name="name",
                address="address",
                city="city",
                country="country",
                website="website",
            )
            self.authors = [
                Author.create(
                    first_name="first_name",
                    last_name="last_name",
                )
            ]
            self.book1 = Book.create(
                title="test book 1",
                description="test book 1 description",
                publication_date=datetime.now(),
                publisher=self.publisher,
            )
            self.book2 = Book.create(
                title="test book 2",
                description="test book 2 description",
                publication_date=datetime.now(),
                publisher=self.publisher,
            )

            self.valid_payload = {
                "title": "Book1",
                "description": "Book1 Description",
                "publication_date": "2022-04-15",
                "publisher_id": self.publisher.id,
                "authors_ids": [item.id for item in self.authors],
            }

            self.invalid_payload = {"title": "", "description": "Book2 Description"}

    def test_valid_update_book(self):
        response = self.client.put(
            reverse("book:book_detail", kwargs={"pk": self.book1.id}),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_book(self):
        response = self.client.put(
            reverse("book:book_detail", kwargs={"pk": self.book2.id}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.json()
        )


class DeleteSingleBookTest(BaseTestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(MODELS, methodName=methodName)

    def setUp(self):
        super().setUp()
        with self.test_db:
            self.publisher = Publisher.create(
                name="name",
                address="address",
                city="city",
                country="country",
                website="website",
            )
            self.authors = [
                Author.create(
                    first_name="first_name",
                    last_name="last_name",
                )
            ]
            self.book1 = Book.create(
                title="test book 1",
                description="test book 1 description",
                publication_date=datetime.now(),
                publisher=self.publisher,
            )
            self.book2 = Book.create(
                title="test book 2",
                description="test book 2 description",
                publication_date=datetime.now(),
                publisher=self.publisher,
            )

    def test_valid_delete_book(self):
        response = self.client.delete(
            reverse("book:book_detail", kwargs={"pk": self.book1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(
            reverse("book:book_detail", kwargs={"pk": self.book1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_delete_book(self):
        response = self.client.delete(reverse("book:book_detail", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
