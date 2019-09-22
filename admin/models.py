from django.db import models

# Create your models here.

class Product(models.Model):
    
 name = models.CharField(max_length="1000"),
 img = models.ImageField(upload_to="pics"),
 price = models.IntegerField(),
 description = models.TextField(),
 status = models.BooleanField(default=True)