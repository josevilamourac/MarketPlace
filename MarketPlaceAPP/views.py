# Create your views here.
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render

from .forms import ProductForm
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
    return render (request, 'MarketPlace/loja.html')
def logout(request):
    return render (request, 'MarketPlace/logout.html')
def dashboard(request):
    return render (request, 'MarketPlace/dashboard.html')


def minha_view(request):
    lojas = Loja.objects.all()  # Query all stores from your database
    return render(request, 'seu_template.html', {'lojas': lojas})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.loja = request.user.loja  # Associa o produto à loja do usuário atual
            product.save()

            # Cria a pasta da loja, se ainda não existir
            store_folder = os.path.join('media', 'store_images', str(request.user.loja.id))
            os.makedirs(store_folder, exist_ok=True)

            # Move a imagem do produto para a pasta da loja
            product_image_path = os.path.join('media', str(product.imagem))
            new_product_image_path = os.path.join(store_folder, os.path.basename(product_image_path))
            os.rename(product_image_path, new_product_image_path)

            return redirect('product_added_successfully')
    else:
        form = ProductForm()
    return render(request, 'MarketPlace/add_product.html', {'form': form})