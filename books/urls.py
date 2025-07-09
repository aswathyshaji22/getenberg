from django.urls import path
from .views import BookListView, RunMigrationsView  

urlpatterns = [
    path('books/', BookListView.as_view()),
    path('run-migrations/', RunMigrationsView.as_view(), name='run-migrations'), 
]
