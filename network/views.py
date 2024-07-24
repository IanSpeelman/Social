from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post
import time

def index(request):
    result = Post.objects.all().order_by("-timestamp")
    p = Paginator(result, 10)
    
    try:
        page = int(request.GET.get("page", 1))
        if page == "" or page < 1:
            page = 1
        elif page > p.num_pages:
            page = p.num_pages
    except:
        page = 1
    posts = p.page(page).object_list
    next = False 
    previous = False
    if page > 1:
        previous = page - 1
    if page < p.num_pages:
        next = page + 1


    if request.method == "POST":
        body = request.POST.get("body", "")
        if body == "":
            return render(request, "network/index.html",{"posts":posts, "next": next, "previous": previous}, status=406)
        if not request.user.is_authenticated:
            return render(request, "network/index.html",{"posts":posts, "next": next, "previous": previous}, status=406)
        newpost = Post(content=body, user=request.user)
        newpost.save()
        return HttpResponseRedirect(reverse(index))

    
    
    
    return render(request, "network/index.html",{
        "posts":posts, 
        "next": next, 
        "previous": previous
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        if len(username) == 0 or len(password) == 0:
            return render(request, "network/login.html", {
                "message": "please fill in all fields."
            }, status=406)
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            }, status=406)
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(confirmation) == 0:
            return render(request, "network/register.html", {
                "message": "Please fill in all fields."
            }, status=406)

        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            }, status=406)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            }, status=406)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


