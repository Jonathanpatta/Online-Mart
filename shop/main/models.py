from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField(max_length=1000,blank=True,null=True)

    price = models.FloatField(null=True,blank=True)
    time_of_creation = models.DateTimeField(auto_now=True,blank=True)
    img = models.ImageField(null=True,blank=True,upload_to="imgs")

    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    user = models.OneToOneField(User, null=True,blank=True,on_delete=models.CASCADE)
    
    otp = models.CharField(max_length=300,null=True,blank=True)
    otp_expiration_date = models.DateTimeField(null=True,blank=True)
    verified = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return str(self.user)


class Order(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
    items = models.ManyToManyField(Item,blank=True)
    Total_price = models.FloatField(blank=True,null=True)

    Cart_json = models.TextField(null=True,blank=True)

    time_of_creation = models.DateTimeField(auto_now=True,blank=True)

    def __str__(self):
        return str(self.user)+str(self.pk)


class UserCart(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
    Cart_json = models.TextField(null=True,blank=True)
    time = models.DateTimeField(auto_now=True,blank=True)

    def __str__(self):
        return str(self.user)+str(self.time)