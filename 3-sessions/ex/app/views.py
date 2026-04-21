import random
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from .forms import SignUpForm, SignInForm, CreateTipForm
from .models import Tip, Vote

User = get_user_model()

def home(request):
    ctx = {}
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CreateTipForm(request.POST)
            if form.is_valid():
                tip = form.save(commit=False)
                tip.author = request.user
                tip.save()
        else:
            form = CreateTipForm()
        ctx["form"] = form

    ctx["tips"] = Tip.objects.all()
    return render(request, "home.html", ctx)

def signup(request):
    ctx = {}
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            if User.objects.filter(username=username):
                messages.info(request, "This username already exists")
            else:
                user = form.save()
                login(request, user)
                messages.success(request, f"Welcome {username} ! Your account was created.")
                return redirect("home")
    else:
        form = SignUpForm()
    ctx["form"] = form
    return render(request, "signup.html", ctx)

def signin(request):
    ctx = {}
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignInForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome {user.username} !")
            return redirect("home")
        else:
            messages.info(request, f"Invalid credentials")
    else:
        form = SignInForm()

    ctx["form"] = form
    return render(request, "signin.html", ctx)

def disconnect(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
    return redirect("home")

def vote(request, tip_id):
    if request.user.is_authenticated:
        tip = get_object_or_404(Tip, id=tip_id)
        nature = int(request.POST.get("nature"))

        current_vote = Vote.objects.filter(tip=tip, author=request.user).first()
        if nature == 2 and (request.user != tip.author and not request.user.has_perm("app.can_downvote")):
            messages.info(request, "You must farm reputation to do that")
            return redirect("home")
        if current_vote and current_vote.nature == nature:
            Vote.objects.filter(tip=tip, author=request.user).delete()
        elif nature == 1 or nature == 2:
            Vote.objects.filter(tip=tip, author=request.user).delete()
            Vote.objects.create(tip=tip, author=request.user, nature=nature)
        else:
            messages.info(request, "How did you do that ?")
    else:
        messages.info(request, "You must have an account to vote")
    return redirect("home")

def destroy(request, tip_id):
    if request.user.is_authenticated: 
        tip = get_object_or_404(Tip, id=tip_id)
        if tip.author == request.user or request.user.has_perm("app.delete_tip"):
            tip.delete()
            messages.info(request, "Tip deleted")
        else:
            messages.info(request, "You are not allowed to do that")
    else:
        messages.info(request, "You must have an account to manage tips")
    return redirect("home")