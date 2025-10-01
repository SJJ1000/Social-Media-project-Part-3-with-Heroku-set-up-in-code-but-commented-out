from django.urls import path
from . import views

app_name = "feed"

urlpatterns = [
    path("", views.home, name="home"),
    path("my-feed/", views.my_feed, name="my_feed"),
    path("friends-feed/", views.friends_feed, name="friends_feed"),
    path("create-post/", views.create_post, name="create_post"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("delete-post/<int:post_id>/", views.delete_post, name="delete_post"),

    
    path("register/", views.register, name="register"),

    
    path("post/<int:post_id>/like/", views.like_post, name="like_post"),
    path("post/<int:post_id>/unlike/", views.unlike_post, name="unlike_post"),

    
    path("friend-requests/", views.friend_requests, name="friend_requests"),
    path("friend-requests/send/", views.send_friend_request, name="send_request_post"),
    path("friend-requests/send/<int:profile_id>/", views.send_friend_request, name="send_request"),
    path("friend-requests/approve/", views.approve_friend_request, name="approve_requests"),
    path("friend-requests/approve/<int:rel_id>/", views.approve_friend_request, name="approve_request"),

    path("my-profile/", views.my_profile, name="my_profile"),
    path("accounts/demo/<str:username>/", views.demo_login, name="demo_login"),

   
    path("relationship/", views.relationship_view, name="relationship"),
]
