from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    #return HttpResponse("Hello World")
    return render(request, "login.html")

def dashboard(request):    
    return render(request, "index.html")

def logout(request):    
    return render(request, "login.html")    