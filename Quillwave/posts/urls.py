from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='index'),
    path('home/', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('search/', views.search, name='search'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('bookmark/<int:post_id>/', views.bookmark_post, name='bookmark_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),

     # ✅ New routes for home.html
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('post/<int:post_id>/', views.view_post, name='view_post')
]
