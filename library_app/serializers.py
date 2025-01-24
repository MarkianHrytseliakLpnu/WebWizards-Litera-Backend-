from rest_framework import serializers
from .models import User, Location, Book, TradeLog, Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'email', 'phone_number']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'address', 'work_schedule']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'location', 'name', 'author', 'publishing', 'year_of_publication', 'language', 'number_of_pages']

class TradeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeLog
        fields = ['id', 'user', 'brought_book', 'borrowed_book', 'location', 'trade_time']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'author', 'book', 'rating', 'response', 'writing_time']