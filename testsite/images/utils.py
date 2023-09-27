from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, FileResponse
from django.core.cache import cache
from .models import Menu, Posts
from .forms import *


def access_wrapper(func):
    """Не даёт зайти в чужой профиль незарегистрированным и другим пользователям"""
    def wrapper(request, username):
        if "username" not in request.session or request.session["username"] != username:
            context = {
                "title": "Unauthorized",
            }
            return render(request, "images/error401.html", context)
        else:
            return func(request, username)
    return wrapper

def profile_wrapper(func):
    """Перенаправляет из /log_in в /users/<имя текущего пользователя>"""
    def wrapper(request):
        if "username" in request.session:
            return redirect(reverse("users", kwargs={"username": request.session["username"]}))
        else:
            return func(request)
    return wrapper


def get_or_create_avatar(request) -> str:
    '''Проверяет аватарку и создаёт её у пользователя в соответствующей бд, если её у него нету'''
    try:
        avatar = Avatars.objects.get(user=request.user).avatar
        return avatar
    except:
        new_avatar = Avatars(user=request.user, avatar="avatars/lappdumb.jpg")
        new_avatar.save()
        avatar = new_avatar.avatar 
        return avatar

def change_avatar(request, form) -> None:
    """Меняет аватарку пользователя"""
    if form.is_valid():
        try:
            form.save()
            avatar = Avatars.objects.get(avatar=form.instance.avatar)
            avatar.user = request.user
        except:
            form.add_error("error")
        else:
            previous = Avatars.objects.filter(user=request.user) #Прежде чем сохранить аватарку, удаляет предыдущую из бд, чтобы не мусорить
            previous.delete()
            avatar.save()

def create_post(request, form) -> None:
    """Отвечает за создание постов"""
    if form.is_valid():
        form_data = form.cleaned_data
        try:
            avatar = Avatars.objects.get(user=request.user).avatar
            post = Posts(username=request.user.username, user=request.user, post_text=form_data["post_text"], avatar=avatar)
        except:
            form.add_error("error")
        else:
            post.save()

def create_bio(request, form):
    """Отвечает за смену био"""
    if form.is_valid():
        form_data = form.cleaned_data
        try:
            bio = Bio(user=request.user, bio=form.cleaned_data["bio"])
        except:
            form.add_error("error")
        else:
            previous = Bio.objects.filter(user=request.user)
            previous.delete()
            bio.save()

def get_or_create_bio(request):
    """Отвечает за получение и создании в противном случае био"""
    try:
        bio = Bio.objects.get(user=request.user).bio
        return bio
    except:
        new_bio = Bio(user=request.user, bio="No Bio")
        new_bio.save()
        bio = new_bio.bio 
        return bio

        