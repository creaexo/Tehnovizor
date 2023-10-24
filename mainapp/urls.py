from django.urls import path
from .views import *
urlpatterns = [
    path('', Menu.as_view(), name='main'),
    path('dish/<str:ct_model>/<str:slug>/', DishView.as_view(), name='dish'),
    path('login', LoginUser.as_view(), name='login'),
    path('cart', CartView.as_view(), name='cart'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('make-order', MakeOrderView.as_view(), name='make_order'),
    path('logout/', logout_user, name='logout'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-form-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_form_cart'),
    path('change-qty/<str:ct_model>/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
]