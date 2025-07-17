from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library

def list_books(request):
    """
    Function-based view that displays all books in the database.
    Shows book titles and their authors in a simple text list.
    """
    books = Book.objects.all()
    context = {
        'books': books,
        'title': 'All Books'
    }
    return render(request, 'relationship_app/list_books.html', context)

# Class-based view to list all libraries
class LibraryListview(ListView):
    """
    Class-based ListView that displays all libraries in the database.
    Shows library names and associated information.
    """
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'

# ✅ Class-based view to display details of a specific library and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.book_set.all()
        return context
