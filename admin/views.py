from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Product

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    #return HttpResponse("Hello World")
    return render(request, "login.html")

def login(request):
    
    if request.method == "POST":
        #return HttpResponse(request.POST.items())
        username = request.POST['username']
        password = request.POST['password']
        #return HttpResponse(username)
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'invalid credential')    
            return redirect('/')
    else:
        messages.info(request, 'invalid post')  
        return redirect('/')        

def dashboard(request):    
    return render(request, "index.html")

def product(request):  

    product_list = Product.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, "product.html",{ 'products': product_list })

def addProduct(request):

    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        img = request.POST['pic']
        
        product = Product(name = name, price = price, description = description, img = img)
        product.save()
        messages.info(request, "Product Craeted Successfully")       

    return render(request, "addProduct.html")

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
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        conf_password = request.POST['conf_password']
        email = request.POST['email']

        if password == conf_password :
            if User.objects.filter(username=username).exists():
                messages.info(request, "User Already Exist")
            elif  User.objects.filter(email=email).exists():
                messages.info(request, "User Already Exist")
            else: 
                user = User.objects.create_user(username = username, password = password, email = email, first_name = first_name, last_name = last_name)
                user.save()
                messages.info(request, "User Craeted Successfully")

        else:
              messages.info(request, "Password shoud be match")          

    return render(request, "addUser.html")

def logout(request):    
    return render(request, "login.html")    