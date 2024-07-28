from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from datetime import datetime
import json
from django.http import JsonResponse
from .models import User,Post,Profile


def index(request):
    if request.method == "POST":
        user = request.user
        content = request.POST["content"]
        timestamp = datetime.now()
        if content != "":
            Post.objects.create(user=user, post=content, timestamp=timestamp)
  
 
    allPosts = Post.objects.all().order_by("timestamp").reverse()
    paginator = Paginator(allPosts, 10)
    pageNumber = request.GET.get('page')
    pageposts = paginator.get_page(pageNumber)
    liked =[]
    try:
        for posts in allPosts:
            current_post = Post.objects.get(pk=posts.id)
            if request.user in current_post.likes.all():
                liked.append(posts.id)
    except:
        liked = []
    return render(request, "network/index.html",{
        "post": pageposts,
        "liked": liked,
    })

def edit(request,id):
    if request.method == "POST":
        data = json.loads(request.body)
        Post.objects.filter(pk=id).update(post=data["post"])
        return JsonResponse({"message": "Success", "data": data["post"]})
 
def like(request,id):
    current_user = request.user
    post = Post.objects.get(pk=id)
    post_likes = post.likes.all()
    if current_user in post_likes:
        post.likes.remove(current_user)
        color="black"
    else:
        post.likes.add(current_user)
        color="red"
 
    return JsonResponse({"message": "Success", "count": post.likes.count(),"color":color})


def profile(request,id):
    user = User.objects.get(pk=id)
    current_user = request.user
    allPosts = Post.objects.filter(user=user).order_by("timestamp").reverse()
    paginator = Paginator(allPosts, 10)
    pageNumber = request.GET.get('page')
    pageposts = paginator.get_page(pageNumber)
    profile_user = Profile.objects.get(user=user)
    profile_viewer = Profile.objects.get(user=current_user)
    profile_followers = profile_user.follower.all()
    if current_user in profile_followers:
        Following = True
    else:
        Following = False
    if request.method == "POST":
        if Following:
           profile_user.follower.remove(current_user)
           profile_viewer.following.remove(user)
           return HttpResponseRedirect(reverse(profile, kwargs={'id':id}))       
        else:
            profile_user.follower.add(current_user)
            profile_viewer.following.add(user)
            return HttpResponseRedirect(reverse(profile, kwargs={'id':id}))  
    liked =[]
    try:
        for posts in allPosts:
            current_post = Post.objects.get(pk=posts.id)
            if request.user in current_post.likes.all():
                liked.append(posts.id)
    except:
        liked = []
    return render(request, "network/profile.html",{
    "post": pageposts,
    "username": user,
    "profile_user":profile_user,
    "following": Following,
    "liked":liked
    })

def following(request):
    current_user = request.user
    user = Profile.objects.get(user=current_user)
    profile_following = user.following.all()
    allPosts = Post.objects.all().order_by("timestamp").reverse()
    followingPost =[] 
    for post in allPosts:
        for people in profile_following:
            if people == post.user:
                followingPost.append(post)

    paginator = Paginator(followingPost, 10)
    pageNumber = request.GET.get('page')
    pageposts = paginator.get_page(pageNumber)
    liked =[]
    try:
        for posts in allPosts:
            current_post = Post.objects.get(pk=posts.id)
            if request.user in current_post.likes.all():
                liked.append(posts.id)
    except:
        liked = []
    return render(request, "network/following.html",{
        "post": pageposts,
        "liked": liked,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
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
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            Profile.objects.create(user=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
