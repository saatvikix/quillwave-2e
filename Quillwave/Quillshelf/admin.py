from django.contrib import admin

# Register your models here.

from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'price', 'published_at')
    search_fields = ('title', 'author__username', 'genre')
    list_filter = ('genre',)
