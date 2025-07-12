# Import the Book model
from bookshelf.models import Book

# Retrieve the book by title
book = Book.objects.get(title="1984")

# Display all attributes
print(f"Book ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
print(f"Full representation: {book}")

# Expected Output
Book ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
Full representation: 1984

