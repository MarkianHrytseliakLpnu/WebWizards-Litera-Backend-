from django.urls import path
from .views import (
    UserListCreateView, UserDetailView,
    BookListCreateView, BookDetailView,
    TradeLogListCreateView, TradeLogDetailView,
    ReviewListCreateView, ReviewDetailView,
    HomeView, BooksView, LocationsView, UserRegisterView
)
from library_app.services.location_service import LocationListCreateView, LocationDetailView
urlpatterns = [
    # Основні URL
    path('', HomeView.as_view(), name='home'),
    path('books/', BooksView.as_view(), name='book'),
    path('locations/', LocationsView.as_view(), name='locations'),
    path('register/', UserRegisterView.as_view(), name='user_register'),

    # API URL
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    path('api/locations/', LocationListCreateView.as_view(), name='location-list-create'),
    path('api/locations/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),

    path('api/books/', BookListCreateView.as_view(), name='book-list-create'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    path('api/tradelogs/', TradeLogListCreateView.as_view(), name='tradelog-list-create'),
    path('api/tradelogs/<int:pk>/', TradeLogDetailView.as_view(), name='tradelog-detail'),

    path('api/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('api/reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
