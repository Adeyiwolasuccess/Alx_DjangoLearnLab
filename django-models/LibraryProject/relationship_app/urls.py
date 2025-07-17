from django.urls import path
from .import views

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view for listing books
    path('books/', views.list_books, name='list_books'),
    
    # Class-based view for listing libraries
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    
    # Function-based view for library detail
    path('library/<int:library_id>/', views.library_detail, name='library_detail'),
    
    # Class-based view for book details
    path('book-details/', views.BookDetailView.as_view(), name='book_detail'),
]