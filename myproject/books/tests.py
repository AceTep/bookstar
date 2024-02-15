from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Book, Author, Publisher
from django.contrib.auth.models import User



class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user
        user = User.objects.create_user(username='testuser', password='12345')

        # Create an author
        author = Author.objects.create(name='Test Author')

        # Create a publisher
        publisher = Publisher.objects.create(name='Test Publisher')

        # Create a book and associate the author and publisher
        book = Book.objects.create(title='Test Book', publication_date='2024-02-14', publisher=publisher, upload_user=user)
        book.authors.add(author)  # Associate the author with the book


    def test_book_title(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.title, 'Test Book')

    def test_book_author(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.authors.first().name, 'Test Author')

    def test_book_publisher(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.publisher.name, 'Test Publisher')

    def test_book_upload_user(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.upload_user.username, 'testuser')


class UserCreationTest(TestCase):
    def test_create_new_user(self):
        # Create a new user
        user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')

        # Check if the user is created successfully
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('12345'))


class AuthorCreationTest(TestCase):
    def test_create_new_author(self):
        # Create a new author
        author = Author.objects.create(name='Test Author', email='test@example.com')

        # Check if the author is created successfully
        self.assertIsNotNone(author)
        self.assertEqual(author.name, 'Test Author')
        self.assertEqual(author.email, 'test@example.com')

