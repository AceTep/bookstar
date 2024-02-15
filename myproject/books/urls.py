from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),  
    path('logout/', views.user_logout, name='logout'),
    
    # Book
    path('add_book/', views.add_book, name='add_book'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_publisher/', views.add_publisher, name='add_publisher'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),

    # Authors
    path('authors/', views.author_list, name='author_list'),
    path('author/add/', views.add_author, name='add_author'),
    path('author/edit/<int:author_id>/', views.author_edit, name='author_edit'),
    path('author/delete/<int:author_id>/', views.author_delete, name='author_delete'),
    path('author/<int:author_id>/', views.author_books, name='author_books'),
    
    # Publishers
    path('publishers/', views.publisher_list, name='publisher_list'),
    path('publisher/add/', views.add_publisher, name='add_publisher'),
    path('publisher/edit/<int:publisher_id>/', views.publisher_edit, name='publisher_edit'),
    path('publisher/delete/<int:publisher_id>/', views.publisher_delete, name='publisher_delete'),
    path('publisher/<int:publisher_id>/', views.publisher_detail, name='publisher_detail'),

]
