from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'is_draft']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'inputs',
                'id': 'titleInput',
                'placeholder': 'Give it a heading',
                'required': True,
            }),
            'body': forms.Textarea(attrs={
                'class': 'inputs',
                'id': 'blog',
                'placeholder': 'Write your blog...',
                'required': True,
                'rows': 10,
            }),
            'image': forms.FileInput(attrs={
                'id': 'fileInput',
                'accept': 'image/*',
            }),
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # ✅ 'text' exists on Comment model
