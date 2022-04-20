"""
Services of Book App
"""
from django.http import Http404
from peewee import Model
from playhouse.shortcuts import model_to_dict
from rest_framework.serializers import Serializer

from book.models import Author, Book, Publisher


class BaseService:
    def __init__(self, model: type[Model], serializer: type[Serializer]) -> None:
        self.serializer = serializer
        self.model = model

    def _get_object(self, pk: str) -> Model:
        try:
            return self.model.get_by_id(pk)
        except self.model.DoesNotExist:
            raise Http404

    def get_object(self, pk: str) -> Model:
        return self._get_object(pk)

    def get_all_objects(self) -> list[Model]:
        return self.model.select().order_by(self.model.id)

    def create_object(self, create_data):
        self.validate_request(create_data)
        new_object = self.model.create(**create_data)
        return True

    def update_object(self, pk: str, update_data) -> bool:
        self.validate_request(update_data)
        object_to_update = self._get_object(pk)

        update_query = self.model.update(**update_data).where(self.model.id == pk)
        update_query.execute()
        return True

    def delete_object(self, pk: str) -> bool:
        object_to_delete = self._get_object(pk)
        object_to_delete.delete_instance()
        return True

    def get_serialized(self, data, many=False) -> Serializer:
        if many:
            serialized = self.serializer(
                data=[
                    model_to_dict(item, recurse=True, backrefs=True, manytomany=True)
                    for item in data
                ],
                many=many,
            )
        else:
            serialized = self.serializer(
                data=model_to_dict(data, recurse=True, backrefs=True, manytomany=True),
                many=False,
            )

        serialized.is_valid(raise_exception=False)
        return serialized

    def validate_request(self, data):
        serialized = self.serializer(data=data)
        serialized.is_valid(raise_exception=True)


class BookService(BaseService):
    def create_book(self, create_data):
        self.validate_request(create_data)

        authors_ids = create_data.pop("authors_ids", None)

        new_book = Book.create(**create_data)
        authors = []
        if authors_ids:
            for id in authors_ids:
                author = Author.get_or_none(id)
                if author:
                    authors.append(author)

        new_book.authors.add(authors)
        return True

    def update_book(self, pk: str, update_data) -> bool:
        self.validate_request(update_data)
        book_to_update = self._get_object(pk)

        authors_ids = update_data.pop("authors_ids", None)

        update_query = Book.update(**update_data).where(Book.id == pk)
        update_query.execute()

        authors = []
        if authors_ids:
            for id in authors_ids:
                author = Author.get_or_none(id)
                if author:
                    authors.append(author)

        book_to_update.authors.clear()
        book_to_update.authors.add(authors)
        return True


class AuthorService(BaseService):
    pass


class PublisherService(BaseService):
    pass
