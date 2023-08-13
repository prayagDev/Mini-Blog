from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, PostForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from .models import Post

# Create your views here.

def home(request):
    posts=Post.objects.all()
    return render(request, "home.html", {"posts":posts})


def signup_user(request):
    if request.method=="POST":
        fm=SignupForm(request.POST)
        if fm.is_valid():
            user=fm.save()
            group=Group.objects.get(name="Author")
            user.groups.add(group)
            return redirect("/login")
    else:
        fm=SignupForm()
    return render(request, "signup.html", {"form":fm})

def login_user(request):
    if request.method=="POST":
        fm=AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname=fm.cleaned_data["username"]
            pwd=fm.cleaned_data["password"]
            user=authenticate(username=uname, password=pwd)
            if user is not None: 
                login(request, user)
                return redirect("/dashboard")
    else:
        fm=AuthenticationForm()
    return render(request, "login.html", {"form":fm})


def dashboard(request):
    user=request.user
    fullName=user.get_full_name()
    grps=user.groups.all()
    if request.method=="POST":
        fm = PostForm(request.POST)
        if fm.is_valid():
            fm.save()
    else:
        fm = PostForm()
    return render(request, "dashboard.html", {"form":fm ,"name":fullName, "groups":grps})

def logout_user(request):
    logout(request)
    return redirect("/login")

def post_delete(request, id):
    post1=Post.objects.get(id=id)
    post1.delete()
    return redirect("/")

def post_update(request, id):
    user=request.user
    fullName=user.get_full_name()
    grps=user.groups.all()
    post1=Post.objects.get(id=id)
    if request.method=="POST":
        fm = PostForm(request.POST, instance=post1)
        if fm.is_valid():
            fm.save()
    else:
        fm = PostForm(instance=post1)
    return render(request, "dashboard.html", {"form":fm ,"name":fullName, "groups":grps})