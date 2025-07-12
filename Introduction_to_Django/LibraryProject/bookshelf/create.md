# Create Operation

## Objective
Create a `Book` instance with the title "1984", author "George Orwell", and publication year 1949.

## Django Shell Commands

```python
# Import the Book model
from bookshelf.models import Book

# Create a new Book instance

book = Book(title="1984", author="George Orwell", publication_year=1949)

# Save the book to the database
book.save()

# Display the created book
print(f"Created book: {book}")
print(f"Book ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

## Expected Output
Created book: 1984
Book ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949

