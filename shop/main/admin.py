from django.contrib import admin
from .models import Item,Profile,Order,UserCart
# Register your models here.

admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(UserCart)
