from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)

    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    x_link = models.URLField(unique=True, blank=True, null=True)
    instagram_link = models.URLField(unique=True, blank=True, null=True)
    telegram_link = models.URLField(unique=True, blank=True, null=True)
    facebook_link = models.URLField(unique=True, blank=True, null=True)

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.username


class Friendship(models.Model):
    class FriendshipStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        ACCEPTED = 'A', 'Accepted'
        DECLINED = 'D', 'Declined'
        BLOCKED = 'B', 'Blocked'

    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships_sent'
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships_received'
    )
    status = models.CharField(
        max_length=1,
        choices=FriendshipStatus.choices,
        default=FriendshipStatus.PENDING
    )
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_from', 'user_to')

    def __str__(self):
        return f"Friendship from {self.user_from} to {self.user_to} ({self.get_status_display()})"


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    work_schedule = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.full_name


class Publishing(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    authors = models.ManyToManyField('Author', related_name='books')
    publishing = models.ForeignKey(Publishing, on_delete=models.SET_NULL, null=True)
    year_of_publication = models.PositiveIntegerField()
    language = models.CharField(max_length=50)
    number_of_pages = models.PositiveIntegerField()
    categories = models.ManyToManyField('Category', related_name='books')

    def __str__(self):
        return self.name


class TradeLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    brought_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='brought_books')
    borrowed_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_books')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    trade_time = models.DateTimeField()

    def __str__(self):
        return f"Trade by {self.user} at {self.trade_time}"


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    response = models.TextField()
    writing_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.book}"
