from django.urls import path
from . import views

urlpatterns = [
    path('', views.quillshelf_home, name='quillshelf_home'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('account/', views.account_view, name='account'),
    path('publish/', views.publish_book, name='publish_book'),
    path('categories/<slug:genre_slug>/', views.books_by_genre, name='category_view'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),



]

#hello world