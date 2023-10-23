from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Employee)
admin.site.register(CartDish)
admin.site.register(Cart)
admin.site.register(Order)