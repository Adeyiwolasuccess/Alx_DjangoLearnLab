# Import the Book model
from bookshelf.models import Book

# Retrieve the book to update
book = Book.objects.get(title="1984")

# Display current title
print(f"Current title: {book.title}")

# Update the title
book.title = "Nineteen Eighty-Four"

# Save the changes to the database
book.save()

# Display updated title
print(f"Updated title: {book.title}")

# Verify the change by retrieving the book again
updated_book = Book.objects.get(id=book.id)
print(f"Verified title from database: {updated_book.title}")

# Expected Output
Current title: 1984
Updated title: Nineteen Eighty-Four
Verified title from database: Nineteen Eighty-Four