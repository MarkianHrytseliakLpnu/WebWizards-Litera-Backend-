from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Location, Book, TradeLog, Review

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LocationSerializer(serializers.ModelSerializer):
    geojson = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['id', 'name', 'address', 'work_schedule', 'latitude', 'longitude', 'geojson','instagram_link']

    def get_geojson(self, obj):
        return {
            "type": "Feature",
            "properties": {
                "name": obj.name,
                "address": obj.address,
                "work_schedule": obj.work_schedule,
                "instagram_link": obj.instagram_link
            },
            "geometry": {
                "type": "Point",
                "coordinates": [float(obj.longitude), float(obj.latitude)]
            }
        }

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class TradeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeLog
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

