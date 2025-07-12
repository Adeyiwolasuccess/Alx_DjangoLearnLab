# Import the Book model
from bookshelf.models import Book

# Display current books before deletion
print("Books before deletion:")
all_books = Book.objects.all()
for book in all_books:
    print(f"- ID: {book.id}, Title: {book.title}, Author: {book.author}")

# Retrieve the book to delete
book = Book.objects.get(title="Nineteen Eighty-Four")  # or whatever the current title is
print(f"\nBook to delete: {book}")

# Delete the book
book.delete()
print("Book deleted successfully!")

# Confirm deletion by retrieving all books
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

# Expected Output
Books before deletion:
- ID: 1, Title: Nineteen Eighty-Four, Author: George Orwell

Book to delete: Nineteen Eighty-Four
Book deleted successfully!

Books after deletion:
No books found in the database.

Total books in database: 0