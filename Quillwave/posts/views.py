from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like, Bookmark
from .forms import PostForm, CommentForm
from django.db.models import Q

def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'index.html')

@login_required
def home(request):
    posts = Post.objects.filter(is_draft=False).order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
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
    return render(request, 'create.html', {'form': form, 'editing': True})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect('home')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('home')

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
    if request.method == 'POST':
        text = request.POST.get('comment')
        if text:
            Comment.objects.create(post=post, author=request.user, text=text)
    return redirect('home')

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

def bookmarks(request):
    # Show posts bookmarked by the user
    return render(request, 'bookmarks.html')

def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'view_post.html', {'post': post})
