"""
Models of Book App
"""
from peewee import CharField, DateField, ForeignKeyField, ManyToManyField, TextField

from db.base import BaseModel


class Publisher(BaseModel):
    """Publisher Model"""

    name = CharField(max_length=30)
    address = CharField(max_length=50)
    city = CharField(max_length=60)
    country = CharField(max_length=50)
    website = CharField(max_length=50)


class Author(BaseModel):
    """Author Model"""

    first_name = CharField(max_length=30)
    last_name = CharField(max_length=40)


class Book(BaseModel):
    """Book Model"""

    title = CharField(max_length=255)
    description = TextField()
    authors = ManyToManyField(Author, "books")
    publisher = ForeignKeyField(Publisher, on_delete="CASCADE")
    publication_date = DateField()

    def __repr__(self):
        return "Book: " + self.title + " is added."

    def __str__(self):
        return f"Book #{self.id}:  {self.title}"
