from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path("", cache_page(60)(Homepage_view.as_view()), name="home"),
    path("home", Homepage_view.as_view(), name="home"),
    path("post/<slug:username>/<int:post_id>", Post_view.as_view(), name="post"),
    path("posts", Posts_view.as_view(), name="posts"),
    path("add_post", AddPost_view.as_view(), name="add_post"),
    path("add_avatar", AddAvatar_view.as_view(), name="add_avatar"),
    path("sign_up", SignUp_view.as_view(), name="sign_up"),
    path("log_in", LogIn_view.as_view(), name="log_in"),
    path("log_out", LogOut_view.as_view(), name="log_out"),
    path("profile", Profile_view.as_view(), name="profile"),
    path("user/<slug:username>", User_view.as_view(), name="user")
]

