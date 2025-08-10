from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Book, Author


class BookCreateAPITests(APITestCase):
    """Test cases for creating books and verifying data integrity"""

    def setUp(self):
        # Create test user & token
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        
        # Create test authors
        self.author_a = Author.objects.create(name="Author A")
        self.create_url = reverse("book-create")

    def test_create_book_success(self):
        """Test creating a book and ensuring data is correctly saved and returned"""
        data = {
            "title": "Test Book Creation",
            "author": self.author_a.id,
            "publication_year": 2023
        }
        
        # Make API request
        response = self.client.post(self.create_url, data, **self.auth_header)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify response data
        self.assertIn('title', response.data)
        self.assertEqual(response.data['title'], "Test Book Creation")
        self.assertEqual(response.data['publication_year'], 2023)
        
        # Verify data is saved in database
        book = Book.objects.get(title="Test Book Creation")
        self.assertEqual(book.title, "Test Book Creation")
        self.assertEqual(book.author, self.author_a)
        self.assertEqual(book.publication_year, 2023)
        
        # Verify database count increased
        self.assertEqual(Book.objects.count(), 1)

    def test_create_book_unauthenticated(self):
        """Test creating book without authentication fails"""
        data = {
            "title": "Unauthorized Book",
            "author": self.author_a.id,
            "publication_year": 2023
        }
        
        response = self.client.post(self.create_url, data)
        
        # Check authentication is required
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify no book was created
        self.assertEqual(Book.objects.count(), 0)

    def test_create_book_invalid_data(self):
        """Test creating book with invalid data returns proper error"""
        data = {
            "title": "",  # Empty title
            "author": 999,  # Non-existent author
            "publication_year": "invalid"  # Invalid year format
        }
        
        response = self.client.post(self.create_url, data, **self.auth_header)
        
        # Check validation error status
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify no book was created
        self.assertEqual(Book.objects.count(), 0)


class BookUpdateAPITests(APITestCase):
    """Test cases for updating books and verifying changes are reflected"""

    def setUp(self):
        # Create test user & token
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        
        # Create test authors and book
        self.author_a = Author.objects.create(name="Author A")
        self.author_b = Author.objects.create(name="Author B")
        self.book = Book.objects.create(
            title="Original Title",
            author=self.author_a,
            publication_year=2020
        )
        self.update_url = reverse("book-update", args=[self.book.id])

    def test_partial_update_book(self):
        """Test partial update (PATCH) and verify changes are reflected"""
        data = {"title": "Updated Title"}
        
        # Make API request
        response = self.client.patch(self.update_url, data, **self.auth_header)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify response data shows update
        self.assertEqual(response.data['title'], "Updated Title")
        
        # Verify changes are reflected in database
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")
        self.assertEqual(self.book.author, self.author_a)  # Unchanged
        self.assertEqual(self.book.publication_year, 2020)  # Unchanged

    def test_full_update_book(self):
        """Test full update (PUT) and verify all changes are reflected"""
        data = {
            "title": "Completely New Title",
            "author": self.author_b.id,
            "publication_year": 2024
        }
        
        # Make API request
        response = self.client.put(self.update_url, data, **self.auth_header)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify response data shows all updates
        self.assertEqual(response.data['title'], "Completely New Title")
        self.assertEqual(response.data['publication_year'], 2024)
        
        # Verify all changes are reflected in database
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Completely New Title")
        self.assertEqual(self.book.author, self.author_b)
        self.assertEqual(self.book.publication_year, 2024)

    def test_update_book_unauthenticated(self):
        """Test updating book without authentication fails"""
        data = {"title": "Should Not Update"}
        
        response = self.client.patch(self.update_url, data)
        
        # Check authentication is required
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify no changes were made to database
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Original Title")

    def test_update_nonexistent_book(self):
        """Test updating non-existent book returns 404"""
        nonexistent_url = reverse("book-update", args=[999])
        data = {"title": "Update Non-existent"}
        
        response = self.client.patch(nonexistent_url, data, **self.auth_header)
        
        # Check proper error status
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookDeleteAPITests(APITestCase):
    """Test cases for deleting books and ensuring removal from database"""

    def setUp(self):
        # Create test user & token
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        
        # Create test author and books
        self.author = Author.objects.create(name="Test Author")
        self.book1 = Book.objects.create(
            title="Book to Delete",
            author=self.author,
            publication_year=2020
        )
        self.book2 = Book.objects.create(
            title="Book to Keep",
            author=self.author,
            publication_year=2021
        )
        self.delete_url = reverse("book-delete", args=[self.book1.id])

    def test_delete_book_success(self):
        """Test deleting a book and ensuring it is removed from database"""
        book_id = self.book1.id
        initial_count = Book.objects.count()
        
        # Make API request
        response = self.client.delete(self.delete_url, **self.auth_header)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify book is removed from database
        self.assertEqual(Book.objects.count(), initial_count - 1)
        self.assertFalse(Book.objects.filter(id=book_id).exists())
        
        # Verify other books remain untouched
        self.assertTrue(Book.objects.filter(id=self.book2.id).exists())

    def test_delete_book_unauthenticated(self):
        """Test deleting book without authentication fails"""
        initial_count = Book.objects.count()
        
        response = self.client.delete(self.delete_url)
        
        # Check authentication is required
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify book still exists in database
        self.assertEqual(Book.objects.count(), initial_count)
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_nonexistent_book(self):
        """Test deleting non-existent book returns 404"""
        nonexistent_url = reverse("book-delete", args=[999])
        
        response = self.client.delete(nonexistent_url, **self.auth_header)
        
        # Check proper error status
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Verify existing books unchanged
        self.assertEqual(Book.objects.count(), 2)


class BookAuthenticationPermissionTests(APITestCase):
    """Test cases for authentication and permission scenarios across all endpoints"""

    def setUp(self):
        # Create test users and tokens
        self.user1 = User.objects.create_user(username="user1", password="pass1")
        self.user2 = User.objects.create_user(username="user2", password="pass2")
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        
        # Auth headers
        self.auth_header1 = {"HTTP_AUTHORIZATION": f"Token {self.token1.key}"}
        self.auth_header2 = {"HTTP_AUTHORIZATION": f"Token {self.token2.key}"}
        
        # Create test data
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            publication_year=2020
        )
        
        # URLs
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", args=[self.book.id])
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update", args=[self.book.id])
        self.delete_url = reverse("book-delete", args=[self.book.id])

    def test_public_read_access(self):
        """Test that read operations (list/detail) are publicly accessible"""
        # Test list endpoint without authentication
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test detail endpoint without authentication
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_protected_write_operations(self):
        """Test that write operations require authentication"""
        test_data = {
            "title": "Unauthorized Book",
            "author": self.author.id,
            "publication_year": 2023
        }
        
        # Test CREATE without auth
        response = self.client.post(self.create_url, test_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test UPDATE without auth
        response = self.client.patch(self.update_url, {"title": "Unauthorized Update"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test DELETE without auth
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_token_access(self):
        """Test that valid tokens allow write operations"""
        # Test CREATE with valid token
        create_data = {
            "title": "Authorized Book",
            "author": self.author.id,
            "publication_year": 2023
        }
        response = self.client.post(self.create_url, create_data, **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Test UPDATE with valid token
        update_data = {"title": "Authorized Update"}
        response = self.client.patch(self.update_url, update_data, **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test DELETE with valid token
        response = self.client.delete(self.delete_url, **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_token_rejection(self):
        """Test that invalid tokens are rejected"""
        invalid_header = {"HTTP_AUTHORIZATION": "Token invalid_token_12345"}
        
        test_data = {
            "title": "Invalid Token Book",
            "author": self.author.id,
            "publication_year": 2023
        }
        
        response = self.client.post(self.create_url, test_data, **invalid_header)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_malformed_authorization_header(self):
        """Test that malformed authorization headers are rejected"""
        malformed_headers = [
            {"HTTP_AUTHORIZATION": "Bearer invalid_format"},
            {"HTTP_AUTHORIZATION": "Token"},  # Missing token
            {"HTTP_AUTHORIZATION": f"InvalidFormat {self.token1.key}"},
        ]
        
        test_data = {
            "title": "Malformed Auth Book",
            "author": self.author.id,
            "publication_year": 2023
        }
        
        for header in malformed_headers:
            response = self.client.post(self.create_url, test_data, **header)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cross_user_permissions(self):
        """Test that different authenticated users can perform operations"""
        # User1 creates a book
        create_data = {
            "title": "User1 Book",
            "author": self.author.id,
            "publication_year": 2023
        }
        response = self.client.post(self.create_url, create_data, **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_book_id = response.data['id']
        
        # User2 can also update the same book (if permissions allow)
        update_url = reverse("book-update", args=[new_book_id])
        update_data = {"title": "Updated by User2"}
        response = self.client.patch(update_url, update_data, **self.auth_header2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookDataValidationTests(APITestCase):
    """Test cases for data validation and response integrity"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Original Book",
            author=self.author,
            publication_year=2020
        )
        
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update", args=[self.book.id])
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", args=[self.book.id])

    def test_create_book_complete_data_verification(self):
        """Test creating book with complete data and verify all fields"""
        data = {
            "title": "Complete Test Book",
            "author": self.author.id,
            "publication_year": 2023
        }
        
        response = self.client.post(self.create_url, data, **self.auth_header)
        
        # Verify status and response structure
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('title', response.data)
        self.assertIn('author', response.data)
        self.assertIn('publication_year', response.data)
        
        # Verify response data matches input
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['publication_year'], data['publication_year'])
        
        # Verify database integrity
        created_book = Book.objects.get(id=response.data['id'])
        self.assertEqual(created_book.title, data['title'])
        self.assertEqual(created_book.author.id, data['author'])
        self.assertEqual(created_book.publication_year, data['publication_year'])

    def test_update_data_integrity(self):
        """Test updating book and verify changes are properly reflected"""
        original_author = self.book.author
        original_year = self.book.publication_year
        
        # Partial update
        update_data = {"title": "Partially Updated Title"}
        response = self.client.patch(self.update_url, update_data, **self.auth_header)
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Partially Updated Title")
        
        # Verify database changes
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Partially Updated Title")
        self.assertEqual(self.book.author, original_author)  # Should remain unchanged
        self.assertEqual(self.book.publication_year, original_year)  # Should remain unchanged

    def test_delete_database_removal(self):
        """Test deleting book and ensure complete removal from database"""
        book_id = self.book.id
        initial_count = Book.objects.count()
        
        delete_url = reverse("book-delete", args=[book_id])
        response = self.client.delete(delete_url, **self.auth_header)
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify complete removal from database
        self.assertEqual(Book.objects.count(), initial_count - 1)
        self.assertFalse(Book.objects.filter(id=book_id).exists())
        
        # Verify subsequent access returns 404
        detail_response = self.client.get(reverse("book-detail", args=[book_id]))
        self.assertEqual(detail_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_response_data_structure(self):
        """Test that list endpoint returns properly structured data"""
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        
        if response.data:  # If books exist
            book_data = response.data[0]
            required_fields = ['id', 'title', 'author', 'publication_year']
            for field in required_fields:
                self.assertIn(field, book_data)

    def test_detail_response_data_structure(self):
        """Test that detail endpoint returns properly structured data"""
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify all required fields are present
        required_fields = ['id', 'title', 'author', 'publication_year']
        for field in required_fields:
            self.assertIn(field, response.data)
        
        # Verify data matches database
        self.assertEqual(response.data['id'], self.book.id)
        self.assertEqual(response.data['title'], self.book.title)
        self.assertEqual(response.data['publication_year'], self.book.publication_year)


class BookSecurityTests(APITestCase):
    """Test cases for security controls and edge cases"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        
        self.author = Author.objects.create(name="Security Author")
        self.book = Book.objects.create(
            title="Security Book",
            author=self.author,
            publication_year=2020
        )

    def test_sql_injection_protection(self):
        """Test that API is protected against SQL injection attempts"""
        # Test with malicious search parameter
        malicious_search = "'; DROP TABLE api_book; --"
        list_url = reverse("book-list")
        
        response = self.client.get(f"{list_url}?search={malicious_search}")
        
        # Should return normal response, not cause server error
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify books table still exists and data is intact
        self.assertTrue(Book.objects.filter(id=self.book.id).exists())

    def test_data_validation_boundaries(self):
        """Test data validation at boundaries"""
        create_url = reverse("book-create")
        
        # Test with extremely long title
        long_title_data = {
            "title": "A" * 1000,  # Very long title
            "author": self.author.id,
            "publication_year": 2023
        }
        response = self.client.post(create_url, long_title_data, **self.auth_header)
        # Should either succeed or return validation error (depends on model constraints)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
        
        # Test with negative publication year
        negative_year_data = {
            "title": "Ancient Book",
            "author": self.author.id,
            "publication_year": -500
        }
        response = self.client.post(create_url, negative_year_data, **self.auth_header)
        # Should handle based on your business logic
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

    def test_token_reuse_after_user_deletion(self):
        """Test that tokens become invalid after user deletion"""
        # Create book with valid token
        create_data = {
            "title": "Valid Token Book",
            "author": self.author.id,
            "publication_year": 2023
        }
        
        response = self.client.post(reverse("book-create"), create_data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Delete the user
        self.user.delete()
        
        # Try to use token after user deletion
        response = self.client.post(reverse("book-create"), create_data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_response_data_consistency(self):
        """Test that response data is consistent across operations"""
        # Create a book
        create_data = {
            "title": "Consistency Test Book",
            "author": self.author.id,
            "publication_year": 2023
        }
        
        create_response = self.client.post(reverse("book-create"), create_data, **self.auth_header)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        
        book_id = create_response.data['id']
        
        # Retrieve the same book
        detail_response = self.client.get(reverse("book-detail", args=[book_id]))
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        
        # Verify data consistency between create and retrieve responses
        create_data_response = create_response.data
        detail_data_response = detail_response.data
        
        self.assertEqual(create_data_response['title'], detail_data_response['title'])
        self.assertEqual(create_data_response['author'], detail_data_response['author'])
        self.assertEqual(create_data_response['publication_year'], detail_data_response['publication_year'])


class BookAPIIntegrationTests(APITestCase):
    """Integration tests that verify complete workflows"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        
        self.author = Author.objects.create(name="Integration Author")

    def test_complete_crud_workflow(self):
        """Test complete CRUD workflow: Create -> Read -> Update -> Delete"""
        
        # 1. CREATE
        create_data = {
            "title": "Workflow Test Book",
            "author": self.author.id,
            "publication_year": 2023
        }
        create_response = self.client.post(reverse("book-create"), create_data, **self.auth_header)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        
        book_id = create_response.data['id']
        self.assertEqual(create_response.data['title'], "Workflow Test Book")
        
        # 2. READ (Verify creation)
        detail_response = self.client.get(reverse("book-detail", args=[book_id]))
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['title'], "Workflow Test Book")
        
        # 3. UPDATE
        update_data = {"title": "Updated Workflow Book"}
        update_response = self.client.patch(
            reverse("book-update", args=[book_id]), 
            update_data, 
            **self.auth_header
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['title'], "Updated Workflow Book")
        
        # Verify update in database
        updated_book = Book.objects.get(id=book_id)
        self.assertEqual(updated_book.title, "Updated Workflow Book")
        
        # 4. DELETE
        delete_response = self.client.delete(
            reverse("book-delete", args=[book_id]), 
            **self.auth_header
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify deletion from database
        self.assertFalse(Book.objects.filter(id=book_id).exists())
        
        # Verify subsequent access returns 404
        final_detail_response = self.client.get(reverse("book-detail", args=[book_id]))
        self.assertEqual(final_detail_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bulk_operations_integrity(self):
        """Test that bulk operations maintain data integrity"""
        # Create multiple books
        books_data = [
            {"title": f"Bulk Book {i}", "author": self.author.id, "publication_year": 2020 + i}
            for i in range(5)
        ]
        
        created_books = []
        for book_data in books_data:
            response = self.client.post(reverse("book-create"), book_data, **self.auth_header)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            created_books.append(response.data['id'])
        
        # Verify all books exist
        self.assertEqual(Book.objects.count(), 5)
        
        # Update all books
        for book_id in created_books:
            update_data = {"title": f"Updated Bulk Book {book_id}"}
            response = self.client.patch(
                reverse("book-update", args=[book_id]), 
                update_data, 
                **self.auth_header
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify all updates
        for book_id in created_books:
            book = Book.objects.get(id=book_id)
            self.assertTrue(book.title.startswith("Updated Bulk Book"))
        
        # Delete all books
        for book_id in created_books:
            response = self.client.delete(
                reverse("book-delete", args=[book_id]), 
                **self.auth_header
            )
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify all deletions
        self.assertEqual(Book.objects.count(), 0)