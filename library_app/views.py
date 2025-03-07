from django.shortcuts import get_object_or_404
from django.views import View

from .search_utils import search_books
from .search_utils import autocomplete_books
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, UserSettingsForm

from .models import Friendship
from django.contrib.auth import get_user_model
import json
import requests

User = get_user_model()

default_avatar = "/static/library_app/images/avatars/default_avatar.png"


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


class LocationsMapView(View):
    def get(self, request):
        response = requests.get(request.build_absolute_uri('/api/locations/'))  # Отримуємо GeoJSON з API
        geojson = response.json() if response.status_code == 200 else {}
        return render(request, 'locations_map.html', {'geojson': json.dumps(geojson)})


class AutocompleteBooksView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        suggestions = autocomplete_books(query)

        return JsonResponse(suggestions, safe=False)


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
    logout(request)
    messages.success(request, "Ви вийшли із системи.")
    return redirect('home')


@login_required
def user_settings_view(request):
    if request.method == "POST":
        form = UserSettingsForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Дані успішно оновлено!")
            return redirect('user_profile')
        else:
            messages.error(request, "Виправте помилки у формі, будь ласка.")
    else:
        form = UserSettingsForm(user=request.user)

    return render(request, 'user_settings.html', {'form': form})


@login_required
def user_profile_view(request):
    edit_mode = False
    if request.method == 'POST':
        if 'edit_mode' in request.POST:
            edit_mode = True
        elif 'username' in request.POST:
            # Оновлення профілю
            request.user.username = request.POST['username']
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.email = request.POST['email']
            request.user.phone_number = request.POST['phone_number']
            request.user.save()
            messages.success(request, 'Ваш профіль було успішно оновлено!')
            return redirect('user_profile')

    return render(request, 'user_profile.html', {'edit_mode': edit_mode})


@require_POST
@login_required
def send_friend_request_ajax(request):
    user_id = request.POST.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Не вказано ID користувача.'})

    recipient = get_object_or_404(User, pk=user_id)

    # Переконуємося, що не надсилається запит самому собі
    if recipient == request.user:
        return JsonResponse({'success': False, 'error': 'Неможливо надіслати запит самому собі.'})

    friendship, created = Friendship.objects.get_or_create(user_from=request.user, user_to=recipient)
    if created:
        return JsonResponse({'success': True, 'message': 'Запит на дружбу відправлено.'})
    else:
        return JsonResponse({'success': False, 'message': 'Запит на дружбу вже існує.'})


@require_POST
@login_required
def respond_friend_request_ajax(request):
    friendship_id = request.POST.get('friendship_id')
    action = request.POST.get('action')  # очікуємо 'accept', 'decline' або 'block'

    if not friendship_id or not action:
        return JsonResponse({'success': False, 'error': 'Недостатньо даних.'})

    friendship = get_object_or_404(Friendship, pk=friendship_id, user_to=request.user)

    if action == 'accept':
        friendship.status = Friendship.FriendshipStatus.ACCEPTED
        msg = 'Запит прийнято.'
    elif action == 'decline':
        friendship.status = Friendship.FriendshipStatus.DECLINED
        msg = 'Запит відхилено.'
    elif action == 'block':
        friendship.status = Friendship.FriendshipStatus.BLOCKED
        msg = 'Користувача заблоковано.'
    else:
        return JsonResponse({'success': False, 'error': 'Невідомий тип дії.'})

    friendship.save()
    return JsonResponse({'success': True, 'message': msg})


@login_required
def ajax_friends(request):
    """
    Повертає список друзів (Friendship з статусом ACCEPTED).
    """
    accepted_friendships = Friendship.objects.filter(
        status=Friendship.FriendshipStatus.ACCEPTED
    ).filter(
        Q(user_from=request.user) | Q(user_to=request.user)
    )
    friends = []
    for friendship in accepted_friendships:
        friend = friendship.user_to if friendship.user_from == request.user else friendship.user_from
        friends.append({
            'id': friend.id,
            'username': friend.username,
            'first_name': friend.first_name,
            'last_name': friend.last_name,
            'avatar': friend.avatar.url if hasattr(friend, 'avatar') and friend.avatar else default_avatar
        })
    return JsonResponse({'results': friends})

@login_required
def ajax_blocked(request):
    blocked_friendships = Friendship.objects.filter(
        user_from=request.user,
        status=Friendship.FriendshipStatus.BLOCKED
    )
    blocked = []
    for friendship in blocked_friendships:
        blocked.append({
            'id': friendship.user_to.id,
            'username': friendship.user_to.username,
            'first_name': friendship.user_to.first_name,
            'last_name': friendship.user_to.last_name,
            'avatar': friendship.user_to.avatar.url if hasattr(friendship.user_to, 'avatar') and friendship.user_to.avatar else default_avatar
        })
    return JsonResponse({'results': blocked})

@login_required
def ajax_friend_requests(request):
    friend_requests = Friendship.objects.filter(
        user_to=request.user,
        status=Friendship.FriendshipStatus.PENDING
    )
    requests_list = []
    for friendship in friend_requests:
        requests_list.append({
            'id': friendship.id,
            'username': friendship.user_from.username,
            'first_name': friendship.user_from.first_name,
            'last_name': friendship.user_from.last_name,
            'avatar': friendship.user_from.avatar.url if hasattr(friendship.user_from, 'avatar') and friendship.user_from.avatar else default_avatar
        })
    return JsonResponse({'results': requests_list})

@login_required
def ajax_search_users(request):
    q = request.GET.get('q', '')
    if q:
        users = User.objects.filter(username__icontains=q).exclude(id=request.user.id)[:10]
    else:
        users = User.objects.none()
    results = []
    for user in users:
        results.append({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'avatar': user.avatar.url if hasattr(user, 'avatar') and user.avatar else default_avatar
        })
    return JsonResponse({'results': results})