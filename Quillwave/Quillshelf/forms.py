# Updated BookForm with proper genre placeholder

from django import forms
from .models import Book  # Use your actual model name

class BookForm(forms.ModelForm):
    # Override the genre field to match the choices in the Book model
    genre = forms.ChoiceField(
        choices=[('', 'Choose a genre')] + Book.GENRE_CHOICES,  # Use model choices
        widget=forms.Select(attrs={
            'class': 'inputs',
            'required': True,
        })
    )

    class Meta:
        model = Book
        fields = ['title', 'genre', 'description', 'cover', 'price']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'inputs',
                'placeholder': "What's your book's title?",
                'required': True,
            }),

            'description': forms.Textarea(attrs={
                'class': 'inputs',
                'placeholder': 'Write a description of your book... (max 600 characters)',
                'required': True,
                'rows': 6,
                'maxlength': 600,
                'onkeyup': 'countChars(this);',
            }),
            'cover': forms.FileInput(attrs={
                'id': 'fileInput',
                'accept': 'image/*',
                'class': 'hidden-file-input',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'inputs',
                'placeholder': 'Price in USD',
                'required': True,
                'min': '0',
                'step': '0.01',
            }),
        }