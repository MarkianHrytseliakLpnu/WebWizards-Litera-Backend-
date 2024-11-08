from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('library_app.urls')),  # Підключення шляхів з додатку library_app
]
