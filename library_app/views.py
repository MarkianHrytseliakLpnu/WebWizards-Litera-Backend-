from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from .search_utils import search_books

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, UserSettingsForm

from .models import Book, TradeLog, Review
from .serializers import BookSerializer, TradeLogSerializer, ReviewSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class BooksView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        books = search_books(query)

        return render(request, 'book.html', {
            'books': books,
            'query': query,
        })


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()
            messages.success(request, "Реєстрація пройшла успішно!")
            return redirect('login')
        else:
            messages.error(request, "Виправте помилки у формі, будь ласка.")
    else:
        form = RegistrationForm()
    return render(request, 'user_register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            messages.success(request, "Вхід виконано успішно!")
            return redirect('home')
        else:
            messages.error(request, "Невірний email або пароль.")
    else:
        form = LoginForm()
    return render(request, 'user_login.html', {'form': form})


def logout_view(request):
    """
    View для виходу користувача із системи.
    """
    logout(request)
    messages.success(request, "Ви вийшли із системи.")
    return redirect('home')


@login_required
def user_settings_view(request):
    """
    Сторінка налаштувань профілю: редагування Ім'я, Прізвище, Email,
    телефон + можливість змінити пароль (старий + два рази новий).
    """
    if request.method == "POST":
        form = UserSettingsForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Дані успішно оновлено!")
            return redirect('user_settings')  # або на сторінку профілю / home
        else:
            messages.error(request, "Виправте помилки у формі, будь ласка.")
    else:
        form = UserSettingsForm(user=request.user)

    return render(request, 'user_settings.html', {'form': form})


@login_required
def user_profile_view(request):
    return render(request, 'user_profile.html')


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
