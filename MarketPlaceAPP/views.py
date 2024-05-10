# Create your views here.
import os

from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import UserForm, UserRegistoForm, AdminForm, LojaForm


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
            os.makedirs(store_folder, exist_ok=True )

            # Move a imagem do produto para a pasta da loja
            product_image_path = os.path.join('media', str(product.imagem))
            new_product_image_path = os.path.join(store_folder, os.path.basename(product_image_path))
            os.rename(product_image_path, new_product_image_path)

            return redirect('product_added_successfully')
    else:
        form = ProductForm()
    return render(request, 'MarketPlace/add_product.html', {'form': form})


def registo_user(request):
    if request.method == 'POST':
        form_user = UserRegistoForm(request.POST)
        form_cliente = UserForm(request.POST)
        if form_user.is_valid() and form_cliente.is_valid():
            user = form_user.save()
            cliente = form_cliente.save(commit=False)
            cliente.user = user
            cliente.save()
            raw_password = form_user.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('MarketPlace:home')
    else:
        form_user = UserRegistoForm()
        form_cliente = UserForm()
    return render(request, 'MarketPlace/registo_user.html', {'form_user': form_user, 'form_cliente': form_cliente})

def registo_admin(request):
    if request.method == 'POST':
        form_user = UserRegistoForm(request.POST)
        form_admin = AdminForm(request.POST)
        if form_user.is_valid() and form_admin.is_valid():
            user = form_user.save()
            admin = form_admin.save(commit=False)
            admin.user = user
            admin.save()
            raw_password = form_user.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('MarketPlace:home')
    else:
        form_user = UserRegistoForm()
        form_admin = UserForm()
    return render(request, 'MarketPlace/registo_admin.html', {'form_user': form_user, 'form_admin': form_admin})

def registo_loja(request):
    if request.method == 'POST':
        form_user = UserRegistoForm(request.POST)
        form_loja = LojaForm(request.POST)
        if form_user.is_valid() and form_loja.is_valid():
            user = form_user.save()
            loja = form_loja.save(commit=False)
            loja.user = user
            loja.save()
            raw_password = form_user.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('MarketPlace:home')
    else:
        form_user = UserRegistoForm()
        form_loja = UserForm()
    return render(request, 'MarketPlace/registo_loja.html', {'form_user': form_user, 'form_loja': form_loja})

