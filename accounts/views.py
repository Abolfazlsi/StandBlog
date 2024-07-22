from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.forms import LoginForm, RegisterForm, UserEdirForm


def user_login(request):
    if request.user.is_authenticated == True:
        return redirect("home:home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data["username"])
            login(request, user)
            return redirect("home:home")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("home:home")


def user_register(request):
    if request.user.is_authenticated:
        return redirect("home:home")
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create(username=form.cleaned_data["username"], email=form.cleaned_data["email"], password=form.cleaned_data["password1"])
            login(request, user)
            return redirect("home:home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def user_edit(request):
    user = request.user
    form = UserEdirForm(instance=user)
    if request.method == "POST":
        form = UserEdirForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("home:home")

    return render(request, "accounts/user_edit.html", {"form": form})
