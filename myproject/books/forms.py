from django import forms
from .models import Book, Author, Publisher, BookComment

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'publisher', 'publication_date']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['authors'].queryset = Author.objects.all()
        self.fields['publisher'].queryset = Publisher.objects.all()  # Populate dropdown with all publishers



class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['salutation', 'name', 'email']

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'address', 'city', 'state_province', 'country', 'website']


class CommentForm(forms.Form):
    comment = forms.CharField(label='Your Comment', widget=forms.Textarea)
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    rating = forms.ChoiceField(label='Your Rating', choices=RATING_CHOICES)
