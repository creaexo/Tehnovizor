from django.shortcuts import redirect
from django.views import View

from mainapp.models import Employee, Cart, Dish


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated == False:
            return redirect('login')
        if request.user.is_authenticated:
            customer = Employee.objects.filter(user=request.user).first()
            if not customer:
                customer = Employee.objects.create(
                    user=request.user,
                )
                cart = Cart.objects.create(owner=customer)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            #if not cart:
                # cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        self.products_to_cart = self.cart.products.all().values('object_id', 'qty')
        self.dishes_to_cart = []
        for i in self.products_to_cart:
            self.dishes_to_cart.append([Dish.objects.filter(id=i['object_id']), i['qty']])
        return super().dispatch(request, *args, **kwargs)