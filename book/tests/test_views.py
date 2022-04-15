import json
from datetime import datetime

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from book.models import Author, Book, Publisher
from book.serializers import BookSerializer

client = Client()


class GetAllBooksTest(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(
            name="name",
            address="address",
            city="city",
            country="country",
            website="website",
        )
        Book.objects.create(
            title="test book 1",
            description="test book 1 description",
            publication_date=datetime.now(),
            publisher=self.publisher,
        )
        Book.objects.create(
            title="test book 2",
            description="test book 2 description",
            publication_date=datetime.now(),
            publisher=self.publisher,
        )

    def test_get_all_books(self):
        # get API response
        response = client.get(reverse("book:book_main"))
        # get data from db
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleBookTest(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(
            name="name",
            address="address",
            city="city",
            country="country",
            website="website",
        )
        self.book1 = Book.objects.create(
            title="test book 1",
            description="test book 1 description",
            publication_date=datetime.now(),
            publisher=self.publisher,
        )
        self.book2 = Book.objects.create(
            title="test book 2",
            description="test book 2 description",
            publication_date=datetime.now(),
            publisher=self.publisher,
        )

    def test_get_valid_single_book(self):
        response = client.get(reverse("book:book_detail", kwargs={"pk": self.book2.pk}))
        book = Book.objects.get(pk=self.book2.pk)
        serializer = BookSerializer(book)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_book(self):
        response = client.get(reverse("book:book_detail", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewBookTest(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(
            name="name",
            address="address",
            city="city",
            country="country",
            website="website",
        )
        self.authors = [
            Author.objects.create(
                first_name="first_name",
                last_name="last_name",
            )
        ]
        self.book1 = Book.objects.create(
            title="test book 1",
            description="test book 1 description",
            publication_date=datetime.now(),
            publisher=self.publisher,
        )
        self.book2 = Book.objects.create(
            title="test book 2",
            description="test book 2 description",
            publication_date=datetime.now(),
            publisher=self.publisher,
        )

        self.valid_payload = {
            "title": "Book1",
            "description": "Book1 Description",
            "publication_date": "2022-04-15",
            "publisher_id": self.publisher.pk,
            "authors_ids": [item.pk for item in self.authors],
        }

        self.invalid_payload = {"title": "", "description": "Book2 Description"}

    def test_create_valid_book(self):
        response = client.post(
            reverse("book:book_main"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_create_invalid_book(self):
        response = client.post(
            reverse("book:book_main"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleBookTest(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(
            name="name",
            address="address",
            city="city",
            country="country",
            website="website",
        )
        self.authors = [
            Author.objects.create(
                first_name="first_name",
                last_name="last_name",
            )
        ]
        self.book1 = Book.objects.create(
            title="test book 1",
            description="test book 1 description",
            publication_date=datetime.now(),
            publisher=self.publisher,
        )
        self.book2 = Book.objects.create(
            title="test book 2",
            description="test book 2 description",
            publication_date=datetime.now(),
            publisher=self.publisher,
        )

        self.valid_payload = {
            "title": "Book1",
            "description": "Book1 Description",
            "publication_date": "2022-04-15",
            "publisher_id": self.publisher.pk,
            "authors_ids": [item.pk for item in self.authors],
        }

        self.invalid_payload = {"title": "", "description": "Book2 Description"}

    def test_valid_update_book(self):
        response = client.put(
            reverse("book:book_detail", kwargs={"pk": self.book1.pk}),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["title"], self.valid_payload["title"])
        self.assertEqual(
            response.data["data"]["description"], self.valid_payload["description"]
        )

    def test_invalid_update_book(self):
        response = client.put(
            reverse("book:book_detail", kwargs={"pk": self.book2.pk}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleBookTest(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(
            name="name",
            address="address",
            city="city",
            country="country",
            website="website",
        )
        self.authors = [
            Author.objects.create(
                first_name="first_name",
                last_name="last_name",
            )
        ]
        self.book1 = Book.objects.create(
            title="test book 1",
            description="test book 1 description",
            publication_date=datetime.now(),
            publisher=self.publisher,
        )
        self.book2 = Book.objects.create(
            title="test book 2",
            description="test book 2 description",
            publication_date=datetime.now(),
            publisher=self.publisher,
        )

    def test_valid_delete_book(self):
        response = client.delete(
            reverse("book:book_detail", kwargs={"pk": self.book1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.delete(
            reverse("book:book_detail", kwargs={"pk": self.book1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_delete_book(self):
        response = client.delete(reverse("book:book_detail", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
