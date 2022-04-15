"""
URLs of Book App
"""
from django.urls import path

from book import views

app_name = "book"
urlpatterns = [
    path("<str:pk>", views.BookDetailAPIView.as_view(), name="book_detail"),
    path("", views.BookListAPIView.as_view(), name="book_main"),
]
