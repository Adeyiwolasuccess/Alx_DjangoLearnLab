# CREATE
Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
# Output: <Book: 1984>

# RETRIEVE
book = Book.objects.get(title="1984")
print(book.title)
print(book.author)
print(book.publication_year)
# Output: 1984, George Orwell, 1949

# UPDATE
book.title = "Nineteen Eighty-Four"
book.save()
# Output: Nineteen Eighty-Four

# DELETE
book.delete()
Book.objects.all()
# Output: <QuerySet []>