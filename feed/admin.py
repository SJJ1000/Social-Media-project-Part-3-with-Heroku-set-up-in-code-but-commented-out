from django.contrib import admin
from .models import Profile, Relationship, Post, Comment, Like

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "first_name", "last_name", "email", "created", "updated")
    search_fields = ("user__username", "first_name", "last_name", "email")

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "status", "created", "updated")
    list_filter = ("status",)
    search_fields = ("sender__user__username", "receiver__user__username")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "description", "date_posted")
    search_fields = ("username__username", "description")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "username", "text", "date_added")
    search_fields = ("post__description", "username__username", "text")

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created")
    list_select_related = ("user", "post")
    search_fields = ("user__username", "post__description")
