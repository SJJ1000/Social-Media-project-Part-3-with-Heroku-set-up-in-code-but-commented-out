from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Profile, Relationship
from .forms import PostForm, ProfileForm, RelationshipForm
from django.shortcuts import get_object_or_404
from django.urls import reverse

def home(request):
    posts = Post.objects.select_related("username").order_by("-date_posted")
    return render(request, "feed/home.html", {"posts": posts})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = request.user  # required by your Post model
            post.save()
            return redirect("feed:home")
    else:
        form = PostForm()
    return render(request, "feed/create_post.html", {"form": form})

@login_required
def my_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("feed:home")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "feed/my_profile.html", {"form": form})

@login_required
def my_feed(request):
    """Only the current user's posts."""
    posts = (Post.objects
             .select_related("username")
             .filter(username=request.user)
             .order_by("-date_posted"))
    return render(request, "feed/my_feed.html", {"posts": posts})

def post_detail(request, post_id):
    """
    Show a single post, its comments, and a form to add a comment.
    Anyone can view; only logged-in users can submit.
    """
    post = get_object_or_404(Post.objects.select_related("username"), id=post_id)
    comments = post.comment_set.select_related("username").order_by("-date_added")

    form = None
    if request.user.is_authenticated:
        if request.method == "POST":
            from .forms import CommentForm
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.username = request.user
                comment.save()
                return redirect(reverse("feed:post_detail", args=[post.id]))
        else:
            from .forms import CommentForm
            form = CommentForm()

    context = {"post": post, "comments": comments, "form": form}
    return render(request, "feed/post_detail.html", context)


    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("feed:home")
    else:
        form = ProfileForm(instance=profile)

    
    return render(request, "feed/My_profile.html", {"form": form})

@login_required
def relationship_view(request):
    me, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = RelationshipForm(request.POST)
        if form.is_valid():
            rel = form.save(commit=False)
            if not getattr(rel, "sender_id", None):
                rel.sender = me
            rel.save()
            return redirect("feed:home")
    else:
        form = RelationshipForm(initial={"sender": me.id})

    return render(request, "feed/relationship.html", {"form": form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, username=request.user)
    # Only allow the user who created it to delete
    if request.method == "POST":
        post.delete()
        return redirect("feed:home")
    return render(request, "feed/delete_post.html", {"post": post})

