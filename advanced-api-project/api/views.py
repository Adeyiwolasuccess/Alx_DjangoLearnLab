from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

# List all books
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny] # Allow any user to view book details

# Create a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can create books

    def create(self, request, *args, **kwargs):
        """
        Override to add custom behavior after validation."
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Book created successfully!",
                "book": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

# Update an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can update books

    def update(self, request, *args, **kwargs):
        """
        Override to customize update behavior
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": "Book updated successfully!",
                "book": serializer.data
            }
        )


# Delete a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer