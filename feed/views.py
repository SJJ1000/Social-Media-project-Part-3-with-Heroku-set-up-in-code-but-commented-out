from django.http import HttpResponse
from .models import Post

def home(request):
    posts = Post.objects.select_related("username").order_by("-date_posted")
    if not posts.exists():
        return HttpResponse("No posts yet. Add one in /admin.", content_type="text/plain")
    lines = [f"{p.date_posted:%Y-%m-%d %H:%M} — {p.username.username}: {p.description}" for p in posts]
    return HttpResponse("Social Feed\n\n" + "\n".join(lines), content_type="text/plain")
