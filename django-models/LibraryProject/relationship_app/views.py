from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Library

#  Function-based view that displays all books
def list_books(request):
    """
    Displays all books in the database.
    Shows book titles and their authors.
    """
    books = Book.objects.all()
    context = {
        'books': books,
        'title': 'All Books'
    }
    return render(request, 'relationship_app/list_books.html', context)

#  Class-based view that lists all libraries
class LibraryListView(ListView):
    """
    Displays all libraries in the database.
    """
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'

#  Class-based view for a specific library and its books
class LibraryDetailView(DetailView):
    """
    Shows details of a specific library and its related books.
    """
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.book_set.all()
        return context

#  Class-based view for a specific book’s details
class BookDetailView(DetailView):
    """
    Shows detailed information about a specific book.
    """
    model = Book
    template_name = "relationship_app/book_detail.html"
    context_object_name = "book"
