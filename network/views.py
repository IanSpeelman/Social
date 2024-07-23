from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    posts = Post.objects.all()
    if request.method == "POST":
        body = request.POST.get("body", "")
        if body == "":
            return render(request, "network/index.html",{"posts":posts}, status=406)
        if not request.user.is_authenticated:
            return render(request, "network/index.html",{"posts":posts}, status=406)

        newpost = Post(content=body, user=request.user)
        newpost.save()
    
    return render(request, "network/index.html",{
        "posts":posts,
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


