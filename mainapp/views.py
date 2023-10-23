from django.shortcuts import render
from django.views import View


# Create your views here.
class Menu(View):
    def get(self, request, *args, **kwargs):
        return render(request, "base.html")

def page_not_found_view(request, exception):
    return render(request, "base.html", status=404)