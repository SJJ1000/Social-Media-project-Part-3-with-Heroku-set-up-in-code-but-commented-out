from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, login

from .models import Post, Profile, Relationship, Like
from .forms import PostForm, ProfileForm, RelationshipForm, RegisterForm, CommentForm

# ----------------------------
# Core feed pages
# ----------------------------
def home(request):
    posts = Post.objects.select_related("username").order_by("-date_posted")

    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(
            Like.objects.filter(user=request.user, post__in=posts)
            .values_list("post_id", flat=True)
        )

    return render(request, "feed/home.html", {"posts": posts, "liked_ids": liked_ids})


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = request.user
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
    posts = (
        Post.objects
        .select_related("username")
        .filter(username=request.user)
        .order_by("-date_posted")
    )
    liked_ids = set(
        Like.objects.filter(user=request.user, post__in=posts)
        .values_list("post_id", flat=True)
    )
    return render(request, "feed/my_feed.html", {"posts": posts, "liked_ids": liked_ids})

# Friends feed
@login_required
def friends_feed(request):
    me = Profile.objects.select_related("user").get(user=request.user)

    accepted = Relationship.objects.filter(
        status='accepted'
    ).filter(
        Q(sender=me) | Q(receiver=me)
    ).select_related('sender__user', 'receiver__user')

    friend_users = []
    for r in accepted:
        friend_profile = r.receiver if r.sender_id == me.id else r.sender
        friend_users.append(friend_profile.user)

    posts = (
        Post.objects
        .select_related("username")
        .filter(username__in=friend_users)
        .order_by("-date_posted")
    )

    liked_ids = set(
        Like.objects.filter(user=request.user, post__in=posts)
        .values_list("post_id", flat=True)
    )

    return render(request, "feed/friends_feed.html", {
        "posts": posts,
        "liked_ids": liked_ids
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related("username"), id=post_id)
    comments = post.comment_set.select_related("username").order_by("-date_added")

    form = None
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.username = request.user
                comment.save()
                return redirect(reverse("feed:post_detail", args=[post.id]))
        else:
            form = CommentForm()

    context = {"post": post, "comments": comments, "form": form}
    return render(request, "feed/post_detail.html", context)

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = post
            c.username = request.user
            c.save()
    return redirect(request.META.get("HTTP_REFERER") or reverse("feed:home"))

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, username=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("feed:home")
    return render(request, "feed/delete_post.html", {"post": post})

# ----------------------------
# Public registration (creates a Profile)
# ----------------------------
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  
            
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    "first_name": form.cleaned_data.get("first_name", "") or "",
                    "last_name": form.cleaned_data.get("last_name", "") or "",
                    "email": form.cleaned_data.get("email", "") or "",
                },
            )
            auth_login(request, user)
            return redirect("feed:home")
    else:
        form = RegisterForm()
    return render(request, "feed/register.html", {"form": form})


def demo_login(request, username):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        u = User.objects.create_user(username=username, password="demo123!", email=f"{username.lower()}@example.com")
        Profile.objects.get_or_create(user=u, defaults={"first_name": username, "last_name": "Demo", "email": u.email})

    user = authenticate(request, username=username, password="demo123!")
    if user is not None:
        login(request, user)
        return redirect("feed:home")
    return redirect("login")

# ----------------------------
# Likes
# ----------------------------
def _back(request, default="feed:home"):
    return request.META.get("HTTP_REFERER") or reverse(default)

@login_required
def like_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        Like.objects.get_or_create(post=post, user=request.user)
    return redirect(_back(request))

@login_required
def unlike_post(request, post_id):
    if request.method == "POST":
        Like.objects.filter(post_id=post_id, user=request.user).delete()
    return redirect(_back(request))


DEMO_USERS = [
    {"username": "JohnDoe",  "first_name": "John",  "last_name": "Doe",  "email": "john@example.com"},
    {"username": "JaneDoe",  "first_name": "Jane",  "last_name": "Doe",  "email": "jane@example.com"},
    {"username": "AlexSmith","first_name": "Alex",  "last_name": "Smith","email": "alex@example.com"},
]

def _ensure_demo_users():
    for s in DEMO_USERS:
        u, created = User.objects.get_or_create(
            username=s["username"],
            defaults={"email": s["email"]}
        )
        if created:
            u.set_password("demo123!")
            u.save()
        Profile.objects.get_or_create(
            user=u,
            defaults={
                "first_name": s["first_name"],
                "last_name": s["last_name"],
                "email": s["email"],
            },
        )

def _seed_incoming_requests(me: Profile):
    demos = Profile.objects.filter(user__username__in=[d["username"] for d in DEMO_USERS]).exclude(id=me.id)
    for demo in demos:
        already = Relationship.objects.filter(
            Q(sender=demo, receiver=me) | Q(sender=me, receiver=demo)
        ).exists()
        if not already:
            Relationship.objects.create(sender=demo, receiver=me, status="sent")

@login_required
def friend_requests(request):
    _ensure_demo_users()
    me = Profile.objects.get(user=request.user)
    _seed_incoming_requests(me)

    accepted = (
        Relationship.objects.filter(status='accepted')
        .filter(Q(sender=me) | Q(receiver=me))
        .select_related('sender__user', 'receiver__user')
    )
    friends = [r.receiver if r.sender_id == me.id else r.sender for r in accepted]

    sent = Relationship.objects.filter(sender=me, status='sent').select_related('receiver__user')
    received = Relationship.objects.filter(receiver=me, status='sent').select_related('sender__user')

    related_ids = {me.id}
    for r in Relationship.objects.filter(Q(sender=me) | Q(receiver=me)).only('sender_id','receiver_id'):
        related_ids.add(r.sender_id); related_ids.add(r.receiver_id)
    candidates = Profile.objects.select_related('user').exclude(id__in=related_ids)

    return render(request, "feed/friend_requests.html", {
        "me": me,
        "friends": friends,
        "sent": sent,
        "received": received,
        "candidates": candidates,
    })

@login_required
def send_friend_request(request, profile_id=None):
    me = Profile.objects.get(user=request.user)
    if request.method == "POST":
        selected = request.POST.getlist("selected_profiles")
        if selected:
            for pid in selected:
                target = get_object_or_404(Profile, id=pid)
                if target.id != me.id:
                    Relationship.objects.get_or_create(sender=me, receiver=target, defaults={"status": "sent"})
            return redirect("feed:friend_requests")

        pid = request.POST.get("profile_id")
        if pid:
            target = get_object_or_404(Profile, id=pid)
            if target.id != me.id:
                Relationship.objects.get_or_create(sender=me, receiver=target, defaults={"status": "sent"})
            return redirect("feed:friend_requests")

        uname = request.POST.get("username")
        if uname:
            target = get_object_or_404(Profile, user__username=uname)
            if target.id != me.id:
                Relationship.objects.get_or_create(sender=me, receiver=target, defaults={"status": "sent"})
            return redirect("feed:friend_requests")

    if profile_id is not None:
        target = get_object_or_404(Profile, id=profile_id)
        if target.id != me.id:
            Relationship.objects.get_or_create(sender=me, receiver=target, defaults={"status": "sent"})
    return redirect("feed:friend_requests")

@login_required
def approve_friend_request(request, rel_id=None):
    me = Profile.objects.get(user=request.user)

    def _accept(r: Relationship):
        r.status = "accepted"
        r.save()
        other = r.sender if r.receiver_id == me.id else r.receiver
        me.friends.add(other.user)
        other.friends.add(me.user)

    if request.method == "POST":
        ids = request.POST.getlist("approve_ids")
        if ids:
            for r in Relationship.objects.filter(id__in=ids, receiver=me, status="sent"):
                _accept(r)
            return redirect("feed:friend_requests")

    if rel_id is not None:
        r = get_object_or_404(Relationship, id=rel_id, receiver=me, status="sent")
        _accept(r)
    return redirect("feed:friend_requests")

@login_required
def relationship_view(request):
    return redirect("feed:friend_requests")
