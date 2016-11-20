#_*_coding:utf-8_*_
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout


def acc_login(request):
    if request.method == "POST":
        user = authenticate(
            username = request.POST.get("username"),
            password = request.POST.get("password")
        )
        if user is not None:
            login(request,user)  #登陆，保存回话状态
            return HttpResponseRedirect("/monitor/")
        else:
            login_err = "Wrong username or password."
            return render(request, "login/login.html", {"login_err":login_err})

    return render(request, "login/login.html")


def acc_logout(request):
    logout(request)  #退出登陆
    return HttpResponseRedirect("/monitor/")