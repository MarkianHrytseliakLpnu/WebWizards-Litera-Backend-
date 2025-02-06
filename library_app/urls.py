from django.urls import path
from .views import (
    BookListCreateView, BookDetailView,
    ReviewListCreateView, ReviewDetailView,
    TradeLogListCreateView, TradeLogDetailView,
    HomeView, BooksView, RegistrationView, LoginView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('books/', BooksView.as_view(), name='book'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/books/', BookListCreateView.as_view(), name='book-list-create'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('api/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('api/reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('api/tradelogs/', TradeLogListCreateView.as_view(), name='tradelog-list-create'),
    path('api/tradelogs/<int:pk>/', TradeLogDetailView.as_view(), name='tradelog-detail'),
]
