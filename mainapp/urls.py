from django.urls import path
from .views import *
urlpatterns = [
    path('', Menu.as_view(), name='main'),
    path('dish/<str:ct_model>/<str:slug>/', DishView.as_view(), name='dish_detail'),
    path('login', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]