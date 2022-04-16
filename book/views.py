"""
Views of Book App
"""
from typing import Any

from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Author, Publisher
from book.serializers import AuthorSerializer, BookSerializer, PublisherSerializer
from book.services import BookService


class BookListAPIView(APIView):
    serializer_class = BookSerializer
    paginator = PageNumberPagination()
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.book_service = BookService(self.serializer_class)

    def get(self, request: Request):
        book_list = self.book_service.get_all_books()

        results: Any = self.paginator.paginate_queryset(
            book_list.data, request, view=self  # type: ignore
        )
        return self.paginator.get_paginated_response(results)

    def post(self, request: Request):
        serializer = self.book_service.create_book(request.data)

        return Response(
            data={
                "message": "Book Created Successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class BookDetailAPIView(APIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.book_service = BookService(self.serializer_class)

    def get(self, request: Request, pk: str, format=None):
        serializer = self.book_service.get_book(pk)
        return Response(serializer.data)

    def put(self, request: Request, pk: str):
        serializer = self.book_service.update_book(pk, request.data)

        return Response(
            {"message": "Book Updated Successfully", "data": serializer.data}
        )

    def delete(self, request: Request, pk: str):
        self.book_service.delete_book(pk)

        return Response({"message": "Book Deleted Successfully"})


class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.order_by("pk").all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.order_by("pk").all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class PublisherListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.order_by("pk").all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class PublisherRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publisher.objects.order_by("pk").all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.AllowAny]
