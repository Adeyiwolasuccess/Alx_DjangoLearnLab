from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from .models import UserProfile
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.views import View
from .models import Book
from .models import Library

# Role-check functions
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Role-based views with access control
@user_passes_test(is_admin)
def admin_view(request):
    """
    Admin-only view for managing the entire library system
    Only accessible to users with 'Admin' role
    """
    total_books = Book.objects.count()
    total_libraries = Library.objects.count()
    all_users = UserProfile.objects.all()
    
    context = {
        'title': 'Admin Dashboard',
        'total_books': total_books,
        'total_libraries': total_libraries,
        'all_users': all_users,
        'user_role': 'Admin'
    }
    return render(request, 'relationship_app/admin_view.html', context)


@user_passes_test(is_librarian)
def librarian_view(request):
    """
    Librarian-only view for managing books and library operations
    Only accessible to users with 'Librarian' role
    """
    books = Book.objects.all()
    libraries = Library.objects.all()
    
    context = {
        'title': 'Librarian Dashboard',
        'books': books,
        'libraries': libraries,
        'user_role': 'Librarian'
    }
    return render(request, 'relationship_app/librarian_view.html', context)


@user_passes_test(is_member)
def member_view(request):
    """
    Member-only view for browsing books and libraries
    Only accessible to users with 'Member' role
    """
    books = Book.objects.all()
    libraries = Library.objects.all()
    
    context = {
        'title': 'Member Dashboard',
        'books': books,
        'libraries': libraries,
        'user_role': 'Member'
    }
    return render(request, 'relationship_app/member_view.html', context)


# Function-based view that displays all books
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


# Function-based view for user registration
def register(request):
    """
    User registration view using Django's UserCreationForm
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})


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
        context["books"] = self.object.books.all()
        return context


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