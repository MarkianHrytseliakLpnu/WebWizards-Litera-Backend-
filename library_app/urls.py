from django.urls import path
from .views import (
    HomeView, BooksView, register_view, login_view,
    logout_view, user_settings_view, user_profile_view,
    AutocompleteBooksView, send_friend_request_ajax,
    respond_friend_request_ajax, ajax_friends, ajax_blocked,
    ajax_friend_requests, ajax_search_users
)

urlpatterns = [
    path('autocomplete/books/', AutocompleteBooksView.as_view(), name='autocomplete_books'),
    path('', HomeView.as_view(), name='home'),
    path('books/', BooksView.as_view(), name='book'),
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
]
