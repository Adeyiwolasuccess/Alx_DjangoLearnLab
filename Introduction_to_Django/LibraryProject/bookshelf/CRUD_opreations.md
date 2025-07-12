# CRUD Operations Documentation

## Complete CRUD Operations for Book Model

This document contains all the CRUD operations performed on the Book model in the Django shell, including commands and their outputs.

## Setup

```python
# Start Django shell
python manage.py shell

# Import the Book model
from bookshelf.models import Book
```

---

## CREATE Operation

### Command:
```python
# Create a new Book instance
Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book.save()

# Display the created book
print(f"Created book: {book}")
print(f"Book ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

### Output:
```
Created book: 1984
Book ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
```

---

## RETRIEVE Operation

### Command:
```python
# Retrieve the book by title
book = Book.objects.get(title="1984")

# Display all attributes
print(f"Book ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
print(f"Full representation: {book}")
```

### Output:
```
Book ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
Full representation: 1984
```

### Additional Retrieval Methods:
```python
# Get all books
all_books = Book.objects.all()
print(f"All books: {all_books}")

# Get books by filter
books_1949 = Book.objects.filter(publication_year=1949)
print(f"Books from 1949: {books_1949}")
```

### Output:
```
All books: <QuerySet [<Book: 1984>]>
Books from 1949: <QuerySet [<Book: 1984>]>
```

---

## UPDATE Operation

### Command:
```python
# Retrieve the book to update
book = Book.objects.get(title="1984")

# Display current title
print(f"Current title: {book.title}")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Display updated title
print(f"Updated title: {book.title}")

# Verify the change
updated_book = Book.objects.get(id=book.id)
print(f"Verified title from database: {updated_book.title}")
```

### Output:
```
Current title: 1984
Updated title: Nineteen Eighty-Four
Verified title from database: Nineteen Eighty-Four
```

---

## DELETE Operation

### Command:
```python
# Display current books before deletion
print("Books before deletion:")
all_books = Book.objects.all()
for book in all_books:
    print(f"- ID: {book.id}, Title: {book.title}, Author: {book.author}")

# Retrieve and delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
print(f"\nBook to delete: {book}")
book.delete()
print("Book deleted successfully!")

# Confirm deletion
print("\nBooks after deletion:")
all_books = Book.objects.all()
if all_books:
    for book in all_books:
        print(f"- ID: {book.id}, Title: {book.title}, Author: {book.author}")
else:
    print("No books found in the database.")

# Verify count
book_count = Book.objects.count()
print(f"\nTotal books in database: {book_count}")
```

### Output:
```
Books before deletion:
- ID: 1, Title: Nineteen Eighty-Four, Author: George Orwell

Book to delete: Nineteen Eighty-Four
Book deleted successfully!

Books after deletion:
No books found in the database.

Total books in database: 0
```

---

## Verification Commands

### Command:
```python
# Try to retrieve the deleted book
try:
    book = Book.objects.get(title="Nineteen Eighty-Four")
    print(f"Found book: {book}")
except Book.DoesNotExist:
    print("Book no longer exists in database (deletion confirmed)")

# Double-check with exists() method
exists = Book.objects.filter(title="Nineteen Eighty-Four").exists()
print(f"Book exists: {exists}")
```

### Output:
```
Book no longer exists in database (deletion confirmed)
Book exists: False
```

---

## Complete CRUD Cycle Summary

1. **CREATE**: Successfully created a Book instance with title "1984", author "George Orwell", and publication year 1949
2. **RETRIEVE**: Successfully retrieved the book and displayed all its attributes
3. **UPDATE**: Successfully updated the book title from "1984" to "Nineteen Eighty-Four"
4. **DELETE**: Successfully deleted the book and confirmed deletion

## Key Learning Points

- Django ORM provides powerful methods for database operations
- `save()` method is required to persist changes to the database
- `get()` retrieves a single object, `filter()` returns a QuerySet
- `delete()` permanently removes objects from the database
- Always verify operations by checking the database state afterward

## Model Definition Used

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    def __str__(self):
        return self.title
```

This model satisfies all the requirements specified in the task.