# library_app/admin.py
from django.contrib import admin
from .models import Book, Author, Category, Publishing, Location, TradeLog, Review, Country

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Publishing)
admin.site.register(Location)
admin.site.register(TradeLog)
admin.site.register(Review)
admin.site.register(Country)
