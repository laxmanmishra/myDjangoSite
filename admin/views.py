from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    #return HttpResponse("Hello World")
    return render(request, "login.html")

def dashboard(request):    
    return render(request, "index.html")

def product(request):  

    user_list = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, "product.html",{ 'users': users })

def user(request):  

    user_list = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, "user.html",{ 'users': users })

def addUser(request):
    return render(request, "addUser.html")

def logout(request):    
    return render(request, "login.html")    