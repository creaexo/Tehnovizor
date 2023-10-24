from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple, AdminFileWidget
from django.utils.safestring import mark_safe

from .models import *
# Register your models here.


# class MeetingAdmin(admin.ModelAdmin):
#     bbq_sauce = Dish.objects.get(dish)
#     # bbq_sauce.dishes.all()
#     print("oioi - "+ str(bbq_sauce.dishes.all()))
    # list_display = ('owner', 'get_nominations', )
    # print('row - ' + str(Cart.products.values()))
#     model = Cart
#     list_display = ['owner', 'products.dish']

admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Employee)
admin.site.register(CartDish)
admin.site.register(Cart)
admin.site.register(Order)