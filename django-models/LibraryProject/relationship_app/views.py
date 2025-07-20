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
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django import forms
from django.views import View
from .models import Book
from .models import Library


@login_required
def list_books(request):
    books = Book.objects.all()
    context = {'books': books, 'title': 'All Books'}
    return render(request, 'relationship_app/list_books.html', context)

@method_decorator(login_required, name='dispatch')
class LibraryListView(ListView):
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'

@method_decorator(login_required, name='dispatch')
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context

@method_decorator(login_required, name='dispatch')
class BookDetailView(DetailView):
    model = Book
    template_name = "relationship_app/book_detail.html"
    context_object_name = "book"

class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('relationship_app:list_books')

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

class RegisterView(View):
    template_name = 'relationship_app/register.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:list_books')
        return render(request, self.template_name, {'form': form})

# ===== Role-Based Views =====

def check_role(role):
    def inner(user):
        return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == role
    return inner

@login_required
@user_passes_test(check_role('Admin'))
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(check_role('Librarian'))
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(check_role('Member'))
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

# Create View
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

# Update View
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('relationship_app:list_books')
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

# Delete View
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app:list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
