from django.db.models import Q
from .models import Book

def search_books(query):
    query = query.strip()
    if not query:
        return Book.objects.all()

    books = Book.objects.all()
    words = query.split()
    final_q = Q()

    for word in words:
        word_q = (
            Q(name__icontains=word) |
            Q(authors__full_name__icontains=word) |
            Q(publishing__name__icontains=word) |
            Q(categories__name__icontains=word) |
            Q(language__icontains=word) |
            Q(location__name__icontains=word) |
            Q(location__address__icontains=word) |
            Q(location__work_schedule__icontains=word)
        )

        if word.isdigit():
            num_value = int(word)
            word_q |= Q(year_of_publication=num_value) | Q(number_of_pages=num_value)

        final_q |= word_q

    return books.filter(final_q).distinct()


