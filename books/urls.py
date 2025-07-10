from django.urls import path
from .views import BookListView

urlpatterns = [
    path('books/', BookListView.as_view()),
    #path('load-books/', LoadBooksView.as_view()),
]
