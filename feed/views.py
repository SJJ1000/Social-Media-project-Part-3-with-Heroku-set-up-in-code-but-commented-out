from django.http import HttpResponse
from .models import Post

def home(request):
    posts = Post.objects.select_related("username").order_by("-date_posted")
    if not posts.exists():
        return HttpResponse("No posts yet. Add one in /admin.", content_type="text/plain")
    lines = [f"{p.date_posted:%Y-%m-%d %H:%M} — {p.username.username}: {p.description}" for p in posts]
    return HttpResponse("Social Feed\n\n" + "\n".join(lines), content_type="text/plain")

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Post, Profile, Relationship
from .forms import PostForm, ProfileForm, RelationshipForm


def home(request):
    posts = Post.objects.select_related("username").order_by("-date_posted")
    return render(request, "feed/home.html", {"posts": posts})


def create_post(request):
    if not request.user.is_authenticated:
        return redirect(f"/admin/login/?next={request.path}")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = request.user  # <- required by your model
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "feed/create_post.html", {"form": form})


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect(f"/admin/login/?next={request.path}")

    
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "feed/edit_profile.html", {"form": form})


def relationship_view(request):
    if not request.user.is_authenticated:
        return redirect(f"/admin/login/?next={request.path}")

    
    me, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = RelationshipForm(request.POST)
        if form.is_valid():
            rel = form.save(commit=False)
            if not getattr(rel, "sender_id", None):
                rel.sender = me
            rel.save()
            return redirect("home")
    else:
        form = RelationshipForm(initial={"sender": me.id})

    return render(request, "feed/relationship.html", {"form": form})



