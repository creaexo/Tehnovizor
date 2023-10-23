from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView

from .forms import LoginUserForm
from .models import *

# Create your views here.
class Menu(View):
    dishes = Dish.objects.filter()
    print(dishes.values())
    def get(self, request, *args, **kwargs):
        return render(request, "base.html", {'dishes':self.dishes})

def page_not_found_view(request, exception):
    return render(request, "base.html", status=404)

class DishView(DetailView):

    def dispatch(self, request, *args, **kwargs):
        self.queryset = Dish._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'dish'
    template_name = 'product.html'
    slug_url_kwarg = 'slug'

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))


    def get_success_url(self):
        return reverse_lazy('main')

def logout_user(request):
    logout(request)
    return redirect('login')