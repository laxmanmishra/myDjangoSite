from io import BytesIO
from reportlab.pdfgen import canvas
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.sessions.models import Session
from .models import Product
from .models import Customer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.core.files.storage import FileSystemStorage


def link_callback(uri, rel):
    """Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL # Typically /static/
    sRoot = settings.STATIC_ROOT # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL # Typically /static/media/
    mRoot = settings.MEDIA_ROOT # Typically /home/userX/project_static/media/
    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri # handle absolute uri (ie: http://some.tld/foo.png)
    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

def render_pdf_view(request):
    template_path = 'user_printer.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response    

def render_pdf_view_e(request):
    template_path = 'user_printer.html'
    #return render(request, template_path)
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="form11.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

    destination = SITE_ROOT+"/pdf/"
    print(destination)
    file = open(destination + "form1.pdf", "w+b")

    # create a pdf
    pisaStatus = pisa.CreatePDF(
    html.encode('utf-8'), dest=file, link_callback=link_callback, encoding='utf-8')
    # if error then show some funy view
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    #return HttpResponse(destination)
    return response


# Create your views here.
def index(request):
    #return HttpResponse("Hello World")
    if request.session.has_key('loggedin'):
        return redirect('dashboard')
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
            request.session['loggedin'] = True 
            return redirect('dashboard')
        else:
            messages.info(request, 'invalid credential')    
            return redirect('/')
    else:
        messages.info(request, 'invalid post')  
        return redirect('/')        

def dashboard(request):    
    return render(request, "index.html")

def customer(request):
    customer_list = Customer.objects.all().order_by('id').reverse()
    paginator = Paginator(customer_list, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    customers = paginator.get_page(page)

    return render(request, "customer.html",{ 'customers': customers })

def addCustomer(request):
    if request.method == "POST":
        #return HttpResponse(request.POST.items())
        name = request.POST['name']
        father_name = request.POST['father_name']
        chassis_no = request.POST['chassis_no']
        date_of_sale = request.POST['date_of_sale']
        month_and_year_manufacture = request.POST['month_and_year_manufacture']
        address = request.POST['address']
        aadhar = request.POST['aadhar']

        customer = Customer(name = name, father_name = father_name, chassisno = chassis_no, date_of_sales_letter = date_of_sale,address = address, aadhar_pdf = aadhar,month_and_year_manufacture =month_and_year_manufacture )
        status= customer.save()


        customer_info = Customer.objects.latest('id')
        template_path = 'initial-form.html'
        context = {'customer': customer_info}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="form11.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        dirname = customer_info.name+' '+str(customer_info.id)
        if not os.path.exists('Document/'+dirname):
            os.mkdir(os.path.join('Document', dirname))

        destination = settings.BASE_DIR+'/Document/'+dirname+'/'
        #return HttpResponse(destination)
        file = open(destination + "intial_form.pdf", "w+b")
        # create a pdf
        pisaStatus = pisa.CreatePDF(
        html.encode('utf-8'), dest=file, link_callback=link_callback, encoding='utf-8')
        # if error then show some funy view
        if pisaStatus.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        Customer.objects.filter(id=customer_info.id).update(initial_form_pdf="intial_form.pdf")
        messages.info(request, "Customer Craeted Successfully")   

    return render(request, "addCustomer.html")    
    
def viewCustomer(request, id):
    customer_info = Customer.objects.get(id=id)
    #return HttpResponse(customer_info)
    if request.method == 'POST' and 'aadhar' in request.FILES and request.FILES['aadhar']:
        aadhar = request.FILES['aadhar']
        dirname = customer_info.name+' '+str(customer_info.id)
        fs = FileSystemStorage(location='document/'+dirname)
        filename = fs.save("aadhar.pdf", aadhar)
        uploaded_file_url = fs.url(filename)
        Customer.objects.filter(id=customer_info.id).update(aadhar_pdf=uploaded_file_url)

    if request.method == 'POST' and 'receipt' in request.FILES and request.FILES['receipt']:
        receipt = request.FILES['receipt']
        dirname = customer_info.name+' '+str(customer_info.id)
        fs = FileSystemStorage(location='document/'+dirname)
        filename = fs.save("tax_receipt.pdf", receipt)
        uploaded_file_url = fs.url(filename)

        Customer.objects.filter(id=customer_info.id).update(tax_reciept_pdf=uploaded_file_url)

    if request.method == 'POST' and 'insurance' in request.FILES and request.FILES['insurance']:
        insurance = request.FILES['insurance']
        dirname = customer_info.name+' '+str(customer_info.id)
        fs = FileSystemStorage(location='document/'+dirname)
        filename = fs.save("insurance.pdf", insurance)
        uploaded_file_url = fs.url(filename)
        Customer.objects.filter(id=customer_info.id).update(insurance_pdf=uploaded_file_url)   
                    
    # return HttpResponse(customer_info)
    return render(request, "viewCustomer.html", { 'customer': customer_info })  

def deleteCustomer(request,id):
    customer_info = Customer.objects.filter(id=id).delete()
    messages.info(request, "Customer delete Successfully")   
    return redirect('customer')


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
    try:
      del request.session['loggedin']
    except:
      pass
    return render(request, "login.html")    