from typing import Any, Dict
from django import http
from rest_framework import generics
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, FileResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from testsite import settings
from .models import Avatars, Menu, Posts
from .forms import *
from .utils import *

class Homepage_view(ListView):
    """Отвечает за вид базовой страницы сайта (в разработке)"""
    model = Menu
    template_name = "images/home.html"
    extra_context = {"title": "Homepage", "menu_selected": 1}

class Posts_view(ListView):
    """Отвечает за страницу с набором постов"""
    model = Posts
    template_name = "images/posts.html"
    extra_context = {"title": "Posts", "menu_selected": 2}
    context_object_name = "posts"
    paginate_by = 5

class Post_view(ListView):
    """Отвечает за просмотр отдельных постов"""
    model = Posts
    template_name = "images/post.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = f"{self.kwargs['username']} Post {self.kwargs['post_id']}"
        context["post"] = Posts.objects.get(username=self.kwargs["username"], pk=self.kwargs["post_id"])
        return context
      
class SignUp_view(CreateView):
    """Отвечает за регистрацию пользователя на сайте"""
    form_class = UserCreationForm
    template_name = "images/sign_up.html"
    success_url = reverse_lazy("log_in")
    extra_context = {"title": "Sign up", "menu_selected": 5}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        get_or_create_bio(self.request) #Создаёт био
        get_or_create_avatar(self.request) #Cоздаёт аватарку у пользователя
        return redirect("profile")
   
class LogIn_view(LoginView):
    """Отвечает за вход пользователя в свой аккаунт"""
    form_class = AuthenticationForm
    template_name = "images/log_in.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return render(request, self.template_name, {"title": "Log in", "form": self.form_class, "menu_selected": 4})
    
class LogOut_view(LoginRequiredMixin, LogoutView):
    """Отвечает за выход пользователя из аккаунта"""

    def get(self, request):
        logout(self.request)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    
class Profile_view(LoginRequiredMixin, View):
    """Отвечает за профиль пользователя"""
    template_name = "images/profile.html"

    def get(self, request):
        bio = get_or_create_bio(request) #Проверка наличия био у пользователя и её создание в противном случае
        avatar = get_or_create_avatar(request) #Проверка наличия аватарки у пользователя и её создание в противном случае
        return render(request, self.template_name, {"avatar": avatar, "title": "Profile", "menu_selected": 3, "form": BioForm({"bio": bio })})
    
    def post(self, request):
        self.form = BioForm(request.POST)
        create_bio(request, self.form)
        return redirect("profile")
    
class User_view(View):
    """Отвечает за просмотр профилей других пользователей"""
    template_name = "images/user.html"
    
    def get(self, request, username):
        user = get_user_model().objects.get(username=username)
        context = {
            "title": f"User {user.username}",
            "user": user,
            "avatar": Avatars.objects.get(user=user).avatar,
            "bio": Bio.objects.get(user=user).bio
        }
        return render(request, self.template_name, context)

    
class AddAvatar_view(LoginRequiredMixin, View):
    """Отвечает за смену аватарки у пользователя"""
    template_name = "images/add_avatar.html"

    def get(self, request):
        self.form = AvatarForm()

        return render(request, self.template_name, {"title": "Add avatar", "form": self.form})

    def post(self, request):
        self.form = AvatarForm(request.POST, request.FILES)
        change_avatar(request, self.form)
        return render(request, "images/add_avatar.html", {"title": "Add avatar", "form": self.form})

class AddPost_view(LoginRequiredMixin, View):
    """Отвечает за добавление постов"""
    template_name = "images/add_post.html"

    def get(self, request):
        self.form = PostForm()
        return render(request, self.template_name, {"title": "Add post", "form": self.form})

    def post(self, request):
        self.form = PostForm(request.POST)
        create_post(request, self.form)
        return render(request, self.template_name, {"title": "Add post", "form": self.form})

def page_not_found(request, exception):
    return render(request, "images/error404.html")
