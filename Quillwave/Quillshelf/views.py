from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book
from users.models import Profile
from django.db.models import Q 

from .forms import BookForm


def quillshelf_home(request):
    books = Book.objects.all().order_by('-published_at')
    return render(request, 'quillshelf/home.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'quillshelf/book_detail.html', {'book': book})


@login_required
def account_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    books = Book.objects.filter(author=user)

    context = {
        'user': user,
        'profile_pic': profile.profile_pic.url if profile.profile_pic else None,
        'location': profile.location,
        'book_count': books.count(),
        'books': books,
    }
    return render(request, 'quillshelf/account.html', context)


@login_required
def publish_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user  # you set the author here
            book.save()
            return redirect('account')
        else:
            print(form.errors)  # temporarily to debug
    else:
        form = BookForm()
    
    return render(request, 'quillshelf/publish.html', {'form': form})





# ======================================



# def category_view(request, category):
#     books = Book.objects.filter(genre=category)
#     return render(request, 'quillshelf/category_books.html', {'books': books, 'category': category})

GENRE_MAP = {
    'fiction-fantasy': 'Fiction/Fantasy',
    'sci-fi': 'Sci-Fi',
    'romance': 'Romance',
    'thriller': 'Thriller',
    'mystery': 'Mystery',
    'other': 'Other',
}
def books_by_genre(request, genre_slug):
    genre_name = GENRE_MAP.get(genre_slug, None)

    if genre_name is None:
        return render(request, 'quillshelf/category_books.html', {'genre': genre_slug, 'books': [], 'user': request.user})

    search_query = request.GET.get('q', '')
    books = Book.objects.filter(genre=genre_name)

    if search_query:
        books = books.filter(Q(title__icontains=search_query))

    books = books.order_by('-published_at')

    return render(request, 'quillshelf/category_books.html', {
        'genre': genre_name,
        'books': books,
        'user': request.user,
        'search_query': search_query,
    })




# ====================cart===================

from django.contrib import messages

def add_to_cart(request, book_id):
    cart = request.session.get('cart', {})

    # If the cart was a list before, convert it to a dictionary
    if isinstance(cart, list):
        cart = {str(book): 1 for book in cart}

    book_id = str(book_id)

    if book_id in cart:
        cart[book_id] += 1
    else:
        cart[book_id] = 1

    request.session['cart'] = cart
    messages.success(request, "Book added to cart.")
    return redirect('view_cart')

def remove_from_cart(request, book_id):
    cart = request.session.get('cart', {})
    book_id = str(book_id)

    if isinstance(cart, list):
        cart = {str(book): 1 for book in cart}

    cart.pop(book_id, None)
    request.session['cart'] = cart
    messages.success(request, "Book removed from cart.")
    return redirect('view_cart')





@login_required
def view_cart(request):
    cart = request.session.get('cart', {})

    # 🔁 Fix: Convert list-style cart (old) to dict-style with default quantity = 1
    if isinstance(cart, list):
        cart = {str(book_id): 1 for book_id in cart}
        request.session['cart'] = cart  # update the session

    if request.method == 'POST':
        if 'checkout' in request.POST:
            request.session['cart'] = {}
            return render(request, 'quillshelf/order_successful.html')

        # Handle quantity update
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                book_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    if quantity > 0:
                        cart[book_id] = quantity
                    else:
                        cart.pop(book_id, None)
                except ValueError:
                    pass

        request.session['cart'] = cart
        return redirect('view_cart')

    # Continue as usual
    books = Book.objects.filter(id__in=cart.keys())
    book_quantities = {int(k): int(v) for k, v in cart.items()}
    total = sum(book.price * book_quantities.get(book.id, 1) for book in books)

    return render(request, 'quillshelf/cart.html', {
        'books': books,
        'quantities': book_quantities,
        'total': total
    })






