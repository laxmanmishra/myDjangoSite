from django.db import models

# Create your models here.

class Product(models.Model):

 name = models.CharField(max_length=100)
 img = models.ImageField(upload_to='pics')
 price = models.IntegerField(default=0)
 description = models.TextField()
 status = models.BooleanField(default=True)