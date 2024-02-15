from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Book, BookComment, Author, Publisher
from .forms import BookForm, AuthorForm, PublisherForm, CommentForm
from django.db.models import  Avg, Count


def home(request):
    books = Book.objects.all()
    form = BookForm()  # Create an instance of BookForm
    books = Book.objects.annotate(avg_rating=Avg('bookcomment__rating')).all()

    return render(request, 'home.html', {'books': books,'form': form})



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
            # Extract the list of authors from the form data
            authors = request.POST.getlist('authors')
            form.cleaned_data['authors'] = authors  # Ensure authors field is set with the list of authors
            if authors:  # Ensure authors list is not empty
                book.authors.set(authors)  # Associate authors with the book
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})




@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})

@login_required
def add_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = PublisherForm()
    return render(request, 'add_publisher.html', {'form': form})

@login_required
def author_list(request):
    authors = Author.objects.all()
    return render(request, 'list_autors.html', {'authors': authors})

@login_required
def author_edit(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'author_edit.html', {'form': form})

@login_required
def author_delete(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == 'POST':
        author.delete()
        return redirect('author_list')
    return render(request, 'author_delete.html', {'author': author})

@login_required
def publisher_list(request):
    publishers = Publisher.objects.all()
    return render(request, 'list_publishers.html', {'publishers': publishers})

@login_required
def publisher_edit(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)
    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            return redirect('publisher_list')
    else:
        form = PublisherForm(instance=publisher)
    return render(request, 'publisher_edit.html', {'form': form})

@login_required
def publisher_delete(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)
    if request.method == 'POST':
        publisher.delete()
        return redirect('publisher_list')
    return render(request, 'publisher_delete.html', {'publisher': publisher})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user != book.upload_user:
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


@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('home')  # Redirect to the home page after deletion
    return render(request, 'delete_book.html', {'book': book})


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    authors = book.authors.all()
    comments = book.bookcomment_set.all().order_by('-created_at')
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment_text = form.cleaned_data['comment']
            new_rating = form.cleaned_data['rating']
            # Create the new comment
            new_comment = BookComment.objects.create(book=book, user=request.user, comment=new_comment_text, rating=new_rating)
            # Update average rating and total ratings for the book
            update_book_ratings(book)
            return redirect('book_detail', book_id=book_id)

    return render(request, 'book_detail.html', {'book': book, 'authors': authors, 'comments': comments, 'form': form})


def update_book_ratings(book):
    # Calculate new average rating and total ratings
    ratings_info = book.bookcomment_set.aggregate(avg_rating=Avg('rating'), total_ratings=Count('rating'))
    avg_rating = ratings_info['avg_rating'] or 0  # Handle case where there are no ratings yet
    total_ratings = ratings_info['total_ratings']
    # Update the book with the new ratings
    book.average_rating = avg_rating
    book.total_ratings = total_ratings
    book.save()


@login_required
def author_books(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    author_books = Book.objects.filter(authors__id=author_id)
    return render(request, 'author_books.html', {'author': author, 'author_books': author_books})

@login_required
def publisher_detail(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    publisher_books = Book.objects.filter(publisher=publisher)
    return render(request, 'publisher_detail.html', {'publisher': publisher, 'publisher_books': publisher_books})