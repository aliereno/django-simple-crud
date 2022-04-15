from django.test import TestCase

from book.models import Book


class BookTest(TestCase):
    """Test module for Book model"""

    def setUp(self):
        Book.objects.create(title="test book 1", description="test book 1 description")
        Book.objects.create(title="test book 2", description="test book 2 description")

    def test_book_model(self):
        book_1 = Book.objects.get(title="test book 1")
        book_2 = Book.objects.get(title="test book 2")
        self.assertEqual(book_1.__repr__(), "Book: test book 1 is added.")
        self.assertEqual(book_2.__repr__(), "Book: test book 2 is added.")
