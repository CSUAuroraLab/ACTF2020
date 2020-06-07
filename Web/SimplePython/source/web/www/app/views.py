from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from app.models import Profile
from django.views.decorators.csrf import csrf_exempt



name = "LQ House"


def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse("profile"))
        return render(request, 'app/index.html', {
            "name": name
        })
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        age = request.POST['age']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("profile"))
        else:
            User.objects.create_user(username=username, password=password)
            _profile = {"username": username, "age": age}
            profile = Profile(profile=_profile)
            profile.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect(reverse("profile"))

@login_required
def profile(request):
    if request.user.username == "admin":
        user_profile = "flag redacted. login as admin on server to get flag."
    else:
        user_profile = "u are not admin."
    return render(request, 'app/profile.html', {
        "name": name,
        "username": request.user,
        "profile": user_profile
    })

@login_required
def details(request):
    if request.user.username == "admin":
        user_profile = "flag redacted. login as admin on server to get flag."
    else:
        user_profile = "u are not admin."
    context = Profile.objects.filter(**request.GET.dict())
    context = context[0].profile
    return render(request, 'app/details.html', {
        "name": name,
        "username": request.user,
        "profile": user_profile,
        "context": context
    })






def log_out(request):
    logout(request)
    return redirect(reverse("index"))


from django.contrib.auth import models


def update_last_login(sender, user, **kwargs):
    pass


models.update_last_login = update_last_login