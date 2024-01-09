from django.db import models

# Create your models here.
class User_Group(models.Model):
    name_Group= models.CharField(max_length=50)

    def __str__(self):
        return self.Name_Group
     
     
class User(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    headshot = models.ImageField(upload_to='user_headshots')
    user_group = models.ForeignKey(User_Group, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='author_headshots')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    stars = models.CharField(max_length=1)
    comment = models.CharField(max_length=250)
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    id_user  = models.ForeignKey(User, on_delete=models.CASCADE)
    

    
