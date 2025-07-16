# relationship_app/query_samples.py

from .models import Author, Book, Library, Librarian

# Query all books by a specific author
def query_books_by_author(author_name):
    """
    Query all books by a specific author using ForeignKey relationship
    """
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return Book.objects.none()

# List all books in a library
def list_books_in_library(library_name):
    """
    List all books in a specific library using ManyToMany relationship
    """
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return Book.objects.none()

# Retrieve the librarian for a library
def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a specific library using OneToOne relationship
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        return librarian
    except Library.DoesNotExist:
        return None