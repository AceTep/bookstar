from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Import the auth views
from books import views

urlpatterns = [
    path('', views.home, name='home'),  # Route the root URL to the home view
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's authentication URLs
    path('books/', include('books.urls')),  # Include the URLs from your 'books' app
    # Other URL patterns for your project...
]
