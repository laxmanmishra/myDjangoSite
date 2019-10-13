from django.db import models

# Create your models here.

class Product(models.Model):
   name = models.CharField(max_length=100)
   img = models.ImageField(upload_to='pics')
   price = models.IntegerField(default=0)
   description = models.TextField()
   status = models.BooleanField(default=True)

class Customer(models.Model):
   name = models.CharField(max_length=250)
   father_name = models.CharField(max_length=250)
   chassisno = models.CharField(max_length=250)
   address = models.TextField()
   date_of_sales_letter = models.DateField(auto_now=False)
   month_and_year_manufacture = models.DateField('YYYYMM') 
   aadhar_pdf = models.FileField(upload_to="aadhar", blank=True)
   initial_form_pdf = models.FileField(upload_to="form", blank=True)
   tax_reciept_pdf = models.FileField(upload_to="tax_reciept", blank=True)
   insurance_pdf = models.FileField(upload_to="insurance", blank=True)
   active = models.BooleanField(default=True)
   created = models.DateTimeField(auto_now_add=True)
   modified = models.DateTimeField(auto_now=True)