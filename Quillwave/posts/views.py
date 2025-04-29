from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like, Bookmark
from .forms import PostForm, CommentForm
from django.db.models import Q

from users.models import Profile

def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'index.html')

@login_required
def home(request):
    posts = Post.objects.filter(is_draft=False).order_by('-created_at')

    for post in posts:
        post.is_liked = post.likes.filter(user=request.user).exists()

    profile = request.user.profile
    profile_pic = profile.profile_pic.url if profile.profile_pic else None

    return render(request, 'home.html', {
        'posts': posts,
        'profile_pic': profile_pic,
    })



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        print("Form data:", request.POST)  # Debug
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            print("Post saved:", post)
            return redirect('home')
        else:
            print("Form errors:", form.errors)  # 🔥 Show form validation issues
    else:
        form = PostForm()
    return render(request, 'create.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'create.html', {
    'form': form,
    'editing': True,
    'filename': post.image.name.split('/')[-1] if post.image else ''
})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect('home')

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



def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'view_post.html', {'post': post})
