from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Book, BookComment
from .forms import BookForm, AuthorForm, PublisherForm, CommentForm


def home(request):
    books = Book.objects.all()
    form = BookForm()  # Create an instance of BookForm
    return render(request, 'home.html', {'books': books, 'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Redirect to a success page.
            return redirect('home')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required
def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.upload_user = request.user
            book.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})




def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the homepage after adding the author
    else:
        form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})

def add_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the homepage after adding the publisher
    else:
        form = PublisherForm()
    return render(request, 'add_publisher.html', {'form': form})

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user != book.upload_user:
        # Redirect to a page indicating unauthorized access
        return redirect('home')

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            # Extract the list of authors from the form data
            authors = request.POST.getlist('authors')
            form.cleaned_data['authors'] = authors  # Ensure authors field is set with the list of authors
            if authors:  # Ensure authors list is not empty
                book = form.save(commit=False)
                book.save()
                form.save_m2m()  # Save many-to-many relationships
                return redirect('home')
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user == book.upload_user:
        book.delete()
    return redirect('home')

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    comments = book.bookcomment_set.all()  # Retrieve all comments for the book
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment_text = form.cleaned_data['comment']
            # Create a new comment associated with the current user and book
            new_comment = BookComment.objects.create(book=book, user=request.user, comment=new_comment_text)
            # Optionally, you can redirect to a success page or refresh the current page
            # return redirect('book_detail', book_id=book_id)
    
    return render(request, 'book_detail.html', {'book': book, 'comments': comments, 'form': form})