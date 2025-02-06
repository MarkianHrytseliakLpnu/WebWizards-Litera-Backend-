from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Book, TradeLog, Review
from .serializers import UserSerializer, BookSerializer, TradeLogSerializer, ReviewSerializer


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class BooksView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'book.html', {'books': books})


class UserRegisterView(View):
    def get(self, request):
        return render(request, 'user_register.html')

    def post(self, request):
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('home')
        else:
            return HttpResponse(f"Помилка: {serializer.errors}", status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(View):
    def get(self, request):
        return render(request, 'user_login.html')


# ---------- Books Endpoints ----------

class BookListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- Reviews Endpoints ----------

class ReviewListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- Rent (TradeLog) Endpoints ----------

class TradeLogListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        tradelogs = TradeLog.objects.all()
        serializer = TradeLogSerializer(tradelogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TradeLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TradeLogDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        tradelog = get_object_or_404(TradeLog, pk=pk)
        serializer = TradeLogSerializer(tradelog)
        return Response(serializer.data)

    def put(self, request, pk):
        tradelog = get_object_or_404(TradeLog, pk=pk)
        serializer = TradeLogSerializer(tradelog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tradelog = get_object_or_404(TradeLog, pk=pk)
        tradelog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
