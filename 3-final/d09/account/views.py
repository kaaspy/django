import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from .forms import login_form

def account(request):
    ctx = {}
    ctx.update(login_form(request))

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        data = json.loads(request.body)
        if data.get("action") == "login" and not request.user.is_authenticated:
            user = authenticate(request, 
                                username=data.get("username"), 
                                password=data.get("password"))
            if user:
                login(request, user)
                return JsonResponse({"auth": True,
                                     "username": user.username})
            else:
                return JsonResponse({"auth": False,
                                     "message": "Invalid credentials"})

        if data.get("action") == "logout" and request.user.is_authenticated:
            logout(request)
            return JsonResponse({"auth": False})
    return render(request, "account.html", ctx)
