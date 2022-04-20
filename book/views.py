"""
Views of Book App
"""
from typing import Any

from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Author, Book, Publisher
from book.serializers import AuthorSerializer, BookSerializer, PublisherSerializer
from book.services import AuthorService, BookService, PublisherService


class BookListAPIView(APIView):
    serializer_class = BookSerializer
    paginator = PageNumberPagination()
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.book_service = BookService(Book, self.serializer_class)

    def get(self, request: Request):
        book_list = self.book_service.get_all_objects()

        results: Any = self.paginator.paginate_queryset(
            self.book_service.get_serialized(book_list, many=True).data, request, view=self  # type: ignore
        )
        return self.paginator.get_paginated_response(results)

    def post(self, request: Request):
        self.book_service.create_book(request.data)

        return Response(
            data={"message": "Book Created Successfully"},
            status=status.HTTP_201_CREATED,
        )


class BookDetailAPIView(APIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.book_service = BookService(Book, self.serializer_class)

    def get(self, request: Request, pk: str, format=None):
        book_object = self.book_service.get_object(pk)
        serialized = self.book_service.get_serialized(book_object)
        return Response(serialized.initial_data)

    def put(self, request: Request, pk: str):
        self.book_service.update_book(pk, request.data)

        return Response({"message": "Book Updated Successfully"})

    def delete(self, request: Request, pk: str):
        self.book_service.delete_object(pk)

        return Response({"message": "Book Deleted Successfully"})


class AuthorListAPIView(APIView):
    serializer_class = AuthorSerializer
    paginator = PageNumberPagination()
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.author_service = AuthorService(Author, self.serializer_class)

    def get(self, request: Request):
        author_list = self.author_service.get_all_objects()

        results: Any = self.paginator.paginate_queryset(
            self.author_service.get_serialized(author_list, many=True).data, request, view=self  # type: ignore
        )
        return self.paginator.get_paginated_response(results)

    def post(self, request: Request):
        self.author_service.create_object(request.data)

        return Response(
            data={"message": "Author Created Successfully"},
            status=status.HTTP_201_CREATED,
        )


class AuthorDetailAPIView(APIView):
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.author_service = AuthorService(Author, self.serializer_class)

    def get(self, request: Request, pk: str, format=None):
        author_object = self.author_service.get_object(pk)
        serialized = self.author_service.get_serialized(author_object)
        return Response(serialized.initial_data)

    def put(self, request: Request, pk: str):
        self.author_service.update_object(pk, request.data)

        return Response({"message": "Author Updated Successfully"})

    def delete(self, request: Request, pk: str):
        self.author_service.delete_object(pk)

        return Response({"message": "Author Deleted Successfully"})


class PublisherListAPIView(APIView):
    serializer_class = PublisherSerializer
    paginator = PageNumberPagination()
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.publisher_service = PublisherService(Publisher, self.serializer_class)

    def get(self, request: Request):
        publisher_list = self.publisher_service.get_all_objects()

        results: Any = self.paginator.paginate_queryset(
            self.publisher_service.get_serialized(publisher_list, many=True).data, request, view=self  # type: ignore
        )
        return self.paginator.get_paginated_response(results)

    def post(self, request: Request):
        self.publisher_service.create_object(request.data)

        return Response(
            data={"message": "Publisher Created Successfully"},
            status=status.HTTP_201_CREATED,
        )


class PublisherDetailAPIView(APIView):
    serializer_class = PublisherSerializer
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.publisher_service = PublisherService(Publisher, self.serializer_class)

    def get(self, request: Request, pk: str, format=None):
        publisher_object = self.publisher_service.get_object(pk)
        serialized = self.publisher_service.get_serialized(publisher_object)
        return Response(serialized.initial_data)

    def put(self, request: Request, pk: str):
        self.publisher_service.update_object(pk, request.data)

        return Response({"message": "Publisher Updated Successfully"})

    def delete(self, request: Request, pk: str):
        self.publisher_service.delete_object(pk)

        return Response({"message": "Publisher Deleted Successfully"})
