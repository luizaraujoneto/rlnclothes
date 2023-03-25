from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


"""
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            # exibir mensagem de erro de autenticação
            pass
    else:
        return render(request, "login.html")
"""
