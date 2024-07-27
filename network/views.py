from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json

from .models import User, Post, Follow, Likes

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
            return render(request, "network/index.html",{"posts":posts, "next": next, "previous": previous, "title": "Index"}, status=406)
        if not request.user.is_authenticated:
            return render(request, "network/index.html",{"posts":posts, "next": next, "previous": previous, "title": "Index"}, status=406)
        newpost = Post(content=body, user=request.user)
        newpost.save()
        return HttpResponseRedirect(reverse(index))

    
    
    
    return render(request, "network/index.html",{
        "posts":posts, 
        "next": next, 
        "previous": previous,
        "title": "Index",
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


def profile(request, user_id):
          
    try:
        profile = User.objects.filter(id=user_id)[0]
        postsresult = Post.objects.filter(user=profile).order_by("-timestamp")
        followed = Follow.objects.filter(follower=request.user.id, followed=user_id)
        
        
        p = Paginator(postsresult, 10)
    
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
        
        if(len(followed) == 1):
            followed = True
        else:
            followed = False
    except:
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "network/profile.html",{
        "profile": profile,
        "posts": posts,
        "followed":followed,
        "followednum": Follow.objects.filter(followed=profile).count(),
        "followernum": Follow.objects.filter(follower=profile).count(),
        "postcount": len(postsresult),
        "next": next,
        "previous":previous,
        "title": "Profile"
        
    })

def follow(request, user_id): 
    if (request.user.is_authenticated ):
            follower = User.objects.filter(id=request.user.id)[0]
            followed = User.objects.filter(id=user_id)[0]
            check = Follow.objects.filter(follower=follower, followed=followed)
            if(len(check) < 1):
                new_follow = Follow.objects.create(follower=follower, followed=followed)
                new_follow.save()
            else:
                check[0].delete()
            return HttpResponseRedirect(reverse("profile", kwargs={"user_id": user_id}))
    else:
        return HttpResponseRedirect(reverse("profile", kwargs={"user_id": user_id}))
        


def followed(request):
    if request.user.is_authenticated:
        follow_list = Follow.objects.filter(follower=request.user)
        users = []
        for user in follow_list:
            users.append(user.followed)
        postsresult = Post.objects.filter(user__in=users).order_by("-timestamp")

        p = Paginator(postsresult, 10)
    
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

        return render(request, 'network/index.html',{
            "posts":posts,
            "title": "Followed",
            "next":next,
            "previous":previous,
        })
    return HttpResponseRedirect(reverse("login"))

def like(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponse({}, status=401)
    try:
        post = Post.objects.filter(pk=post_id)
        like = Likes.objects.filter(user=request.user, post=post[0])
        new_like = Likes(user=request.user, post=post[0])
        if like:
            like.delete()
        else:
            new_like.save()

        return HttpResponse({}, status=200)
        
    except:
        return HttpResponse({}, status=404)
    
def postinfo(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        likes = Likes.objects.filter(post=post)
        liked_by = False
        for like in likes:
            if like.user == request.user:
                liked_by = True
        return HttpResponse(json.dumps({"post": post_id, "likes":len(likes), "likedByUser": liked_by}), content_type="application/json", status=200)
        
    except:
        return HttpResponse(json.dumps({"message": "post does not exist"}), content_type="application/json", status=404)

def edit(request, post_id):
    if request.method == "POST":
        content = request.POST.get("content", "")
        user = request.user
        title = request.POST.get("title", "index")
        try:
            post = Post.objects.get(id=post_id)
            if post.user == request.user:
                try:
                    post.content = content
                    post.save()
                except:
                    return HttpResponseRedirect(reverse("index"), status=500)
                    
            else:
                return HttpResponseRedirect(reverse("index"), status=403)
        except:
                return HttpResponseRedirect(reverse("index"), status=404)


        #redirect user to the page they came from
        if title == "Profile":
            return HttpResponseRedirect(reverse(title.lower(), kwargs={"user_id":user.id}))
        else:
            return HttpResponseRedirect(reverse("index"))

    return HttpResponseRedirect(reverse("index"), status=405)