from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.views import View
from .models import Book
from .models import Library

@login_required
def list_books(request):
    """
    Displays all books in the database.
    Shows book titles and their authors.
    Requires user to be logged in.
    """
    books = Book.objects.all()
    context = {
        'books': books,
        'title': 'All Books'
    }
    return render(request, 'relationship_app/list_books.html', context)


# Class-based view that lists all libraries
@method_decorator(login_required, name='dispatch')
class LibraryListView(ListView):
    """
    Displays all libraries in the database.
    Requires user to be logged in.
    """
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'


# Class-based view for a specific library and its books
@method_decorator(login_required, name='dispatch')
class LibraryDetailView(DetailView):
    """
    Shows details of a specific library and its related books.
    Requires user to be logged in.
    """
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()  # Using the related name from your models
        return context


class CustomLoginView(LoginView):
    """
    Custom login view using Django's built-in LoginView
    """
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('list_books')


class CustomLogoutView(LogoutView):
    """
    Custom logout view using Django's built-in LogoutView
    """
    template_name = 'relationship_app/logout.html'


class RegisterView(View):
    """
    User registration view using Django's UserCreationForm
    """
   
# Class-based view for a specific book's details
@method_decorator(login_required, name='dispatch')
class BookDetailView(DetailView):
    """
    Shows detailed information about a specific book.
    Requires user to be logged in.
    """
    model = Book
    template_name = "relationship_app/book_detail.html"
    context_object_name = "book"