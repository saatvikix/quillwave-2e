from django.shortcuts import render, redirect
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like, Bookmark
from .forms import PostForm, CommentForm
from django.db.models import Q
from users.models import Profile
import json
import requests
from django.conf import settings

from types import SimpleNamespace


def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'index.html')


@login_required
def home(request):
    posts = Post.objects.filter(is_draft=False).order_by('-created_at')
    for post in posts:
        post.is_liked = post.likes.filter(user=request.user).exists()

    profile_pic = None
    if hasattr(request.user, 'profile') and request.user.profile.profile_pic:
        profile_pic = request.user.profile.profile_pic.url

    return render(request, 'home.html', {
        'posts': posts,
        'profile_pic': profile_pic,
    })




@login_required
def create_post(request):
    
    """
    Handle the creation of a new post by the authenticated user.

    This view renders a form for creating a new post. If the request method is POST, it 
    processes the form data and sends a POST request to the external Flask API to store 
    the post details. If the form is valid, the user is redirected to the home page. 
    Otherwise, the form is re-rendered with any validation errors.

    Returns:
        HttpResponse: Renders the 'create.html' template with the post form.
    """

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
                'body': form.cleaned_data['body'],
                'is_draft': form.cleaned_data['is_draft'],
                'author_id': request.user.id
            }
            files = {}
            image = form.cleaned_data.get('image')
            if image:
                files['image'] = image

            resp = requests.post(
                settings.FLASK_API_BASE,
                data=data,
                files=files
            )
            resp.raise_for_status()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    # Fetch the existing post via API
    resp = requests.get(f"{settings.FLASK_API_BASE}/{post_id}")
    resp.raise_for_status()
    post_data = resp.json()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
                'body': form.cleaned_data['body'],
                'is_draft': form.cleaned_data['is_draft'],
                'author_id': post_data['author_id']
            }
            files = {}
            image = form.cleaned_data.get('image')
            if image:
                files['image'] = image

            resp = requests.put(
                f"{settings.FLASK_API_BASE}/{post_id}",
                data=data,
                files=files
            )
            resp.raise_for_status()
            return redirect('home')
    else:
        form = PostForm(initial={
            'title': post_data['title'],
            'body': post_data['body'],
            'is_draft': post_data['is_draft'],
        })

    return render(request, 'create.html', {
        'form': form,
        'editing': True,
        'filename': post_data.get('image', '').split('/')[-1] if post_data.get('image') else ''
    })


@login_required
def delete_post(request, post_id):
    # Relay deletion via Flask API
    resp = requests.delete(f"{settings.FLASK_API_BASE}/{post_id}")
    if resp.status_code not in (200, 204):
        # handle error if needed
        pass
    return redirect('home')


@login_required
def view_post(request, post_id):
    # Fetch single post from Flask API
    resp = requests.get(f"{settings.FLASK_API_BASE}/{post_id}")
    resp.raise_for_status()
    post = resp.json()
    return render(request, 'view_post.html', {'post': post})








@login_required
def like_post(request, post_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post = Post.objects.get(pk=post_id)
        user = request.user

        liked = False
        existing_like = Like.objects.filter(post=post, user=user).first()

        if existing_like:
            existing_like.delete()
        else:
            Like.objects.create(post=post, user=user)
            liked = True

        like_count = post.likes.count()

        return JsonResponse({
            'liked': liked,
            'likes': like_count
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def bookmark_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    bookmark, created = Bookmark.objects.get_or_create(post=post, user=request.user)
    if not created:
        bookmark.delete()
    return redirect('home')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == "POST":
        text = request.POST.get('content')  # Get the comment content
        if text:
            # Create the new comment
            comment = Comment.objects.create(post=post, author=request.user, text=text)
            # Return a response with the comment and user info
            return JsonResponse({
                "user": request.user.username,  # Or any user attribute you'd like
                "content": comment.text,
            })
        else:
            return JsonResponse({"error": "No comment text provided"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def search(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(body__icontains=query),
        is_draft=False
    ).order_by('-created_at')
    return render(request, 'home.html', {'posts': posts, 'search_query': query})

#PLACEHOLDERS====================================

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')



@login_required
def bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    saved_posts = Post.objects.filter(id__in=bookmarks.values('post_id')).select_related('author').prefetch_related('likes', 'comments')

    for post in saved_posts:
        try:
            post.profile_pic = post.author.profile.profile_pic.url
        except:
            post.profile_pic = None
        post.is_liked = request.user in post.likes.all()

    return render(request, 'bookmarks.html', {'saved_posts': saved_posts})




