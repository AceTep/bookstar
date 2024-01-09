from django.contrib import admin
from .models import *

model_list = [User_Group, User, Publisher, Author, Book, Category, Comment]

admin.site.register(model_list)

# Register your models here.
