from django.urls import path
from . import views
from .views import list_books
from django.contrib.auth.views import LogoutView
from .views import (
    LibraryListView, 
    LibraryDetailView, 
    BookDetailView, 
    library_detail
)

app_name = 'relationship_app'

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('libraries/', LibraryListView.as_view(), name='library_list'),
    
    path('library/<int:library_id>/', library_detail, name='library_detail'),
    path('book-details/', BookDetailView.as_view(), name='book_detail'),

    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]

