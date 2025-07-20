from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import admin_view
from .views import librarian_view
from .views import member_view
from . import views
from .views import add_book
from .views import edit_book
from .views import delete_book

urlpatterns = [
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  
    path('register/', views.register, name='register'),
    
    # Book and Library views (require login)
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),

    path('admin-role/', admin_view, name='admin_view'),
    path('librarian-role/', librarian_view, name='librarian_view'),
    path('member-role/', member_view, name='member_view'),

    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:pk>/', edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', delete_book, name='delete_book'),
]