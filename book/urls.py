"""
URLs of Book App
"""
from django.urls import path

from book import views

app_name = "book"
urlpatterns = [
    path("book/<str:pk>", views.BookDetailAPIView.as_view(), name="book_detail"),
    path("book/", views.BookListAPIView.as_view(), name="book_main"),
    path(
        "author/<str:pk>",
        views.AuthorRetrieveUpdateDestroyAPIView.as_view(),
        name="author_detail",
    ),
    path("author/", views.AuthorListCreateAPIView.as_view(), name="author_main"),
    path(
        "publisher/<str:pk>",
        views.PublisherRetrieveUpdateDestroyAPIView.as_view(),
        name="publisher_detail",
    ),
    path(
        "publisher/", views.PublisherListCreateAPIView.as_view(), name="publisher_main"
    ),
]
