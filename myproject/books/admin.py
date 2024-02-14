from django.contrib import admin
from .models import *

# Register your models here.
model_list = [Publisher, Author, Book, BookComment]

admin.site.register(model_list)