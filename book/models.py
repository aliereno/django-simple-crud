"""
Models of Book App
"""
from django.db import models


class Publisher(models.Model):
    """Publisher Model"""

    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=50)
    website = models.URLField()


class Author(models.Model):
    """Author Model"""

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)


class Book(models.Model):
    """Book Model"""

    title = models.CharField(max_length=255)
    description = models.TextField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "Book: " + self.title + " is added."

    def __str__(self):
        return f"Book #{self.pk}:  {self.title}"
