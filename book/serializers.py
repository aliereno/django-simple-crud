"""
Serializers of Book App
"""
from rest_framework import serializers


class PublisherSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=30)
    address = serializers.CharField(max_length=50)
    city = serializers.CharField(max_length=60)
    country = serializers.CharField(max_length=50)
    website = serializers.CharField(max_length=50)


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=40)


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=225, required=True)
    description = serializers.CharField(required=True)
    publication_date = serializers.DateField(required=True)

    authors = AuthorSerializer(many=True, read_only=True)
    publisher = PublisherSerializer(read_only=True)
    publisher_id = serializers.IntegerField(write_only=True, required=True)
    authors_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
