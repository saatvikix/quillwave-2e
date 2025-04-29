from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    GENRE_CHOICES = [
       
        ('Fiction/Fantasy', 'Fiction/Fantasy'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Romance', 'Romance'),
        ('Thriller', 'Thriller'),
        ('Mystery', 'Mystery'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='book_covers/')
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
