from django.urls import path
from .views import (
    UserListCreateView, UserDetailView,
    LocationListCreateView, LocationDetailView,
    BookListCreateView, BookDetailView,
    TradeLogListCreateView, TradeLogDetailView,
    ReviewListCreateView, ReviewDetailView
)

urlpatterns = [
    # User URLs
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Location URLs
    path('locations/', LocationListCreateView.as_view(), name='location-list-create'),
    path('locations/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),

    # Book URLs
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # TradeLog URLs
    path('tradelogs/', TradeLogListCreateView.as_view(), name='tradelog-list-create'),
    path('tradelogs/<int:pk>/', TradeLogDetailView.as_view(), name='tradelog-detail'),

    # Review URLs
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
