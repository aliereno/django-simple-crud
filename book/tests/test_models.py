from datetime import datetime

from peewee import *

from book.models import Author, Book, Publisher
from book.tests import BaseTestCase

MODELS = [Author, Book, Publisher, Book.authors.get_through_model()]


class BookModelTest(BaseTestCase):
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
                    first_name="first_name1",
                    last_name="last_name1",
                ),
                Author.create(
                    first_name="first_name2",
                    last_name="last_name2",
                ),
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
            self.book2.authors.add(*self.authors)

    def test_book_model(self):
        self.assertEqual(self.book1.__repr__(), "Book: test book 1 is added.")
        self.assertEqual(self.book2.__repr__(), "Book: test book 2 is added.")
