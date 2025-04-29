from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Comment, Like, Bookmark

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_email', 'created_at', 'is_draft')
    search_fields = ('title', 'body', 'author__email')
    list_filter = ('is_draft', 'created_at')

    def author_email(self, obj):
        return obj.author.email
    author_email.short_description = 'Author Email'

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Bookmark)
