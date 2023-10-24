from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.contrib import messages
from .forms import LoginUserForm, OrderForm
from .mixins import CartMixin
from .models import *
from .utils import recalc_cart


# Create your views here.
class Menu(CartMixin, View):
    dishes = Dish.objects.filter()
    # print(dishes.values())
    def get(self, request, *args, **kwargs):
        return render(request, "base.html", {'dishes':self.dishes, 'cart':self.cart,})

def page_not_found_view(request, exception):
    return render(request, "base.html", status=404)

class DishView(CartMixin, DetailView):

    def dispatch(self, request, *args, **kwargs):
        self.queryset = Dish._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'dish'
    template_name = 'product.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))


    def get_success_url(self):
        return reverse_lazy('main')

class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        products_to_cart = self.cart.products.all().values('object_id','qty')
        dishes_to_cart = []
        for i in products_to_cart:
            dishes_to_cart.append([Dish.objects.filter(category__dish__id=i['object_id']),i['qty']])
        print('erwerwerwer  -  '+str(products_to_cart))
        print(dishes_to_cart)

        context = {
            'cart': self.cart,
            'dishes_to_cart': dishes_to_cart
        }
        return render(request, 'cart.html', context)
# class AddToCartView(CartMixin,View):
#
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
#             content_type = ContentType.objects.get(model=ct_model)
#             product = content_type.model_class().objects.get(slug=product_slug)
#             quantity = request.GET.get("quantity")
#             try:
#                 check_product_in_cart = CartDish.objects.get(
#                     user=self.cart.owner,
#                     cart=self.cart,
#                     content_type=content_type,
#                     object_id=product.id)
#             except:
#                 check_product_in_cart = False
#                 print(check_product_in_cart)
#             if(check_product_in_cart):
#                 check_product_in_cart.qty += int(quantity)
#                 check_product_in_cart.save()
#             else:
#                 cart_product, created = CartDish.objects.get_or_create(
#                     user=self.cart.owner,
#                     cart=self.cart,
#                     content_type=content_type,
#                     qty=int(quantity),
#                     object_id=product.id,
#                     # glist=f"Правый глаз: sph={right_sph}, cyl={right_cyl}, ax={right_ax}; Левый глаз: sph={left_sph}, cyl={left_cyl}, ax={left_ax}; pd1={pd1}, pd2={pd2}"
#                 )
#                 if created:
#                     self.cart.products.add(cart_product)
#                     print(f"created = {created}")
#
#             print(f"quantity = {quantity}")
#
#
#             recalc_cart(self.cart)
#
#             messages.add_message(request, messages.INFO, "Товар добавленв корзину")
#             return HttpResponseRedirect('/cart/')
#
#         else:
#             messages.add_message(request, messages.INFO, "Чтобы добавить товар, пожалуйста, авторизируйтесь!")
#             return HttpResponseRedirect('/login')
def logout_user(request):
    logout(request)
    return redirect('login')

class AddToCartView(CartMixin,View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = Dish.objects.filter(category__dish__slug=kwargs.get('slug'))
            print('product --- ' + str(product.values()))
            quantity = request.GET.get("quantity")
            try:
                check_product_in_cart = CartDish.objects.get(
                    user=self.cart.owner,
                    cart=self.cart,
                    object_id=product[0].id)
            except:
                check_product_in_cart = False
                print(check_product_in_cart)
            if(check_product_in_cart):
                check_product_in_cart.qty += int(quantity)
                check_product_in_cart.save()
            else:
                cart_product, created = CartDish.objects.get_or_create(
                    user=self.cart.owner,
                    cart=self.cart,
                    qty=int(quantity),
                    dish=product[0],
                    object_id=product[0].id,
                )
                if created:
                    self.cart.products.add(cart_product)
                    print(f"created = {created}")

            print(f"quantity = {quantity}")


            recalc_cart(self.cart)

            messages.add_message(request, messages.INFO, "Товар добавленв корзину")
            return HttpResponseRedirect('/cart')

        else:
            messages.add_message(request, messages.INFO, "Чтобы добавить товар, пожалуйста, авторизируйтесь!")
            return HttpResponseRedirect('/login')


class DeleteFromCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        product = Dish.objects.filter(category__dish__slug=kwargs.get('slug'))
        cart_product = CartDish.objects.get(
            user=self.cart.owner, cart=self.cart, object_id=product[0].id
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удалён")
        return HttpResponseRedirect('/cart')


class CheckoutView(CartMixin, View):
    def get(self, request, *args, **kwargs):

        form = OrderForm(request.POST or None)
        # products_order = request.POST
        products_to_cart = self.cart.products.all().values('object_id','qty','final_price')
        dishes_to_cart = []
        for i in products_to_cart:
            dishes_to_cart.append([Dish.objects.filter(category__dish__id=i['object_id']),i['qty'],i['final_price']])

        context = {
            'cart': self.cart,
            'form': form,
            'dishes_to_cart': dishes_to_cart
        }
        return render(request, 'checkout.html', context, **kwargs)

class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product = Dish.objects.filter(category__dish__slug=kwargs.get('slug'))

        cart_product = CartDish.objects.get(
            user=self.cart.owner,
            cart=self.cart,
            object_id=product[0].id)
        qty = int(request.POST.get('quantity'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Кол-во успешно изменено")
        print(request.POST)
        return HttpResponseRedirect('/cart')

class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        form = OrderForm(request.POST or None)
        customer = Employee.objects.get(user=request.user)
        for i in form:
            print(i)
        if form.is_valid():
            recalc_cart(self.cart)

            new_order = form.save(commit=False)
            new_order.employee = customer
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.order_time = form.cleaned_data['order_time']
            new_order.comment = form.cleaned_data['comment']
            new_order.products_information = form.cleaned_data['products_information']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)

            self.cart = Cart.objects.create(owner=customer)




            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout')