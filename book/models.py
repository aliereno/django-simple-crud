"""
Models of Book App
"""
from django.db import models


class Book(models.Model):
    """Book Model"""

    title = models.CharField(max_length=255)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "Book: " + self.title + " is added."

    def __str__(self):
        return f"Book #{self.pk}:  {self.title}"
