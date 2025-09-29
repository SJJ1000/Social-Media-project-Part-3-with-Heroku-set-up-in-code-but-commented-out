from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create-post/", views.create_post, name="create_post"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("relationship/", views.relationship_view, name="relationship"),
]
