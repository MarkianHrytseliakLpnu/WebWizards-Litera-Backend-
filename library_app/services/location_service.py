from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from library_app.models import Location
from library_app.serializers import LocationSerializer

class LocationListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)

        # Перетворюємо всі локації в GeoJSON FeatureCollection
        geojson = {
            "type": "FeatureCollection",
            "features": [location["geojson"] for location in serializer.data]
        }

        return Response(geojson)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocationDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def put(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)