# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Loja

def index(request):
    return HttpResponse("Pagina de entrada da app votacao.")
def home(request):
    return render (request, 'MarketPlace/home.html')
def login(request):
    return render (request, 'MarketPlace/login.html')
def contact(request):
    return render (request, 'MarketPlace/contact.html')
def perfil(request):
    return render (request, 'MarketPlace/perfil.html')
def carrinho(request):
    return render (request, 'MarketPlace/carrinho.html')
def loja(request):
    lojas = Loja.objects.all()  # Query all stores from your database
    return render(request, 'MarketPlace/loja.html', {'lojas': lojas})
def logout(request):
    return render (request, 'MarketPlace/logout.html')
def dashboard(request):
    return render (request, 'MarketPlace/dashboard.html')



