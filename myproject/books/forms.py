from django import forms
from .models import Book, Author, Publisher

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'publisher', 'publication_date', 'comments']  # Include 'comments' field
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),  # Textarea for comments
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['authors'].queryset = Author.objects.all()  # Populate dropdown with all authors
        self.fields['publisher'].queryset = Publisher.objects.all()  # Populate dropdown with all publishers



class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['salutation', 'name', 'email']  # Adjust fields as needed

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'address', 'city', 'state_province', 'country', 'website']  # Adjust fields as needed


class CommentForm(forms.Form):
    comment = forms.CharField(label='Your comment', widget=forms.Textarea)