from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} {self.surname}"


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brought_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='brought_books')
    borrowed_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_books')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    trade_time = models.DateTimeField()

    def __str__(self):
        return f"Trade by {self.user} at {self.trade_time}"


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    response = models.TextField()
    writing_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author} for {self.book}"
