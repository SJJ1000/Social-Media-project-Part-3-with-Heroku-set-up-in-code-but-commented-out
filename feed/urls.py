from django.urls import path
from . import views

app_name = "feed"

urlpatterns = [
    path("", views.home, name="home"),
    path("create-post/", views.create_post, name="create_post"),
    path("my-feed/", views.my_feed, name="my_feed"),                       
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),   
    path("relationship/", views.relationship_view, name="relationship"),
    path("my-profile/", views.my_profile, name="my_profile"),
    path("delete-post/<int:post_id>/", views.delete_post, name="delete_post")
]
