from django.urls import path
from .views import (
    BookListCreateView, BookDetailView,
    ReviewListCreateView, ReviewDetailView,
    TradeLogListCreateView, TradeLogDetailView,
    HomeView, BooksView, register_view, login_view,LocationsMapView,
    logout_view, user_settings_view, user_profile_view
    HomeView, BooksView, register_view, login_view,
    logout_view, user_settings_view, user_profile_view,
    AutocompleteBooksView, send_friend_request_ajax,
    respond_friend_request_ajax, ajax_friends, ajax_blocked,
    ajax_friend_requests, ajax_search_users
)
from library_app.services.location_service import LocationListCreateView
urlpatterns = [
    path('autocomplete/books/', AutocompleteBooksView.as_view(), name='autocomplete_books'),
    path('', HomeView.as_view(), name='home'),
    path('books/', BooksView.as_view(), name='book'),
    path('locations/', LocationsMapView.as_view(), name='locations_map'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('settings/', user_settings_view, name='user_settings'),
    path('profile/', user_profile_view, name='user_profile'),
    path('ajax/friend-request/send/', send_friend_request_ajax, name='ajax_send_friend_request'),
    path('ajax/friend-request/respond/', respond_friend_request_ajax, name='ajax_respond_friend_request'),
    path('ajax/friends/', ajax_friends, name='ajax_friends'),
    path('ajax/blocked/', ajax_blocked, name='ajax_blocked'),
    path('ajax/friend_requests/', ajax_friend_requests, name='ajax_friend_requests'),
    path('ajax/search_users/', ajax_search_users, name='ajax_search_users'),
    path('api/books/', BookListCreateView.as_view(), name='book-list-create'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('api/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('api/reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('api/tradelogs/', TradeLogListCreateView.as_view(), name='tradelog-list-create'),
    path('api/tradelogs/<int:pk>/', TradeLogDetailView.as_view(), name='tradelog-detail'),
    path('api/locations/', LocationListCreateView.as_view(), name='location-list-create')
]
