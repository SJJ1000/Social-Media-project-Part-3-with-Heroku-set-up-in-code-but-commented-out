from django.contrib import admin
from .models import Profile, Relationship, Post, Comment, Like

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "first_name", "last_name", "email", "created", "updated")
    search_fields = ("user__username", "first_name", "last_name", "email")
    filter_horizontal = ("friends",)

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "status", "created", "updated")
    list_filter = ("status",)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "description", "date_posted")
    search_fields = ("description", "username__username")
    ordering = ("-date_posted",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "username", "text", "date_added")
    search_fields = ("text", "username__username")
    ordering = ("-date_added",)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "post")
    search_fields = ("username__username",)
