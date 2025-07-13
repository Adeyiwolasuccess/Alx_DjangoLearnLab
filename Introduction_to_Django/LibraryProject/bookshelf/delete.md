from bookshelf.models import Book

# Display current books before deletion
print("Books before deletion:")
for book in Book.objects.all():
    print(f"- {book.title} by {book.author}")

# Retrieve and delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion
print("Books after deletion:")
print(Book.objects.all())

# Output
Books before deletion:
- Nineteen Eighty-Four by George Orwell
Books after deletion:
<QuerySet []>
