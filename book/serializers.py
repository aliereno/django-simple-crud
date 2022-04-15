"""
Serializers of Book App
"""
from rest_framework import serializers

from book.models import Author, Book, Publisher


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    publisher = PublisherSerializer(read_only=True)
    publisher_id = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.all(), write_only=True
    )
    authors_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Author.objects.all(), write_only=True
    )

    class Meta:
        model = Book
        fields = "__all__"

    def create(self, validated_data):
        validated_data["publisher"] = validated_data.pop("publisher_id", None)
        validated_data["authors"] = validated_data.pop("authors_ids", None)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["publisher"] = validated_data.pop("publisher_id", None)
        validated_data["authors"] = validated_data.pop("authors_ids", None)

        return super().update(instance, validated_data)
