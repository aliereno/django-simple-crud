from datetime import datetime

from django.test import TestCase

from book.models import Author, Book, Publisher


class BookTest(TestCase):
    """Test module for Book model"""

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
                first_name="first_name1",
                last_name="last_name1",
            ),
            Author.objects.create(
                first_name="first_name2",
                last_name="last_name2",
            ),
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
        self.book2.authors.add(*self.authors)

    def test_book_model(self):
        book_1 = Book.objects.get(title="test book 1")
        book_2 = Book.objects.get(title="test book 2")
        self.assertEqual(book_1.__repr__(), "Book: test book 1 is added.")
        self.assertEqual(book_2.__repr__(), "Book: test book 2 is added.")
