from rest_framework import serializers
from .models import User, Location, Book, TradeLog, Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'email', 'phone_number']

class LocationSerializer(serializers.ModelSerializer):
    geojson = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['id', 'name', 'address', 'work_schedule', 'latitude', 'longitude', 'geojson']

    def get_geojson(self, obj):
        return {
            "type": "Feature",
            "properties": {
                "name": obj.name,
                "address": obj.address,
                "work_schedule": obj.work_schedule
            },
            "geometry": {
                "type": "Point",
                "coordinates": [float(obj.longitude), float(obj.latitude)]
            }
        }

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