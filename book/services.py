"""
Services of Book App
"""
from django.http import Http404
from rest_framework.serializers import Serializer

from book.models import Book


class BookService:
    def __init__(self, serializer: type[Serializer]) -> None:
        self.serializer = serializer

    def _get_book_object(self, pk: str) -> Book:
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get_book(self, pk: str) -> Serializer:
        return self.serializer(self._get_book_object(pk))

    def get_all_books(self) -> Serializer:
        return self.serializer(Book.objects.order_by("pk").all(), many=True)

    def create_book(self, create_data) -> Serializer:
        serializer = self.serializer(data=create_data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return serializer

    def update_book(self, pk: str, update_data) -> Serializer:
        book_to_update = self._get_book_object(pk)

        serializer = self.serializer(
            instance=book_to_update, data=update_data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

    def delete_book(self, pk: str) -> bool:
        book_to_delete = self._get_book_object(pk)
        book_to_delete.delete()
        return True
