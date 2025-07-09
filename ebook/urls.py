from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # 👈 Add this import

urlpatterns = [
    path('', lambda request: redirect('/api/books/')),  # 👈 Redirect root URL
    path('admin/', admin.site.urls),
    path('api/', include('books.urls')),
    path('api/', include('books.urls')),
]
