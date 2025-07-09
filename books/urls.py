from django.urls import path
from .views import BookListView, RunMigrationsView, LoadBooksView

urlpatterns = [
    path('books/', BookListView.as_view()),
    path('run-migrations/', RunMigrationsView.as_view(), name='run-migrations'), 
    path('load-books/', LoadBooksView.as_view()),
]
