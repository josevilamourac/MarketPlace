# Create your views here.
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render

from .forms import ProductForm
from .models import Loja


def index(request):
    return HttpResponse("Pagina de entrada da app votacao.")


def home(request):
    lojas = Loja.objects.all()  # Recupera todos os objetos de loja do banco de dados
    return render(request, 'MarketPlace/home.html', {'lojas': lojas})


def login(request):
    return render(request, 'MarketPlace/login.html')


def contact(request):
    return render(request, 'MarketPlace/contact.html')


def perfil(request):
    return render(request, 'MarketPlace/perfil.html')


def carrinho(request):
    return render(request, 'MarketPlace/carrinho.html')


def loja(request, store_id):
    loja = get_object_or_404(Loja, id=store_id)
    descricao_loja = loja.descricao
    return render(request, 'MarketPlace/loja.html', {'store_id': store_id, 'descricao_loja': descricao_loja})


def logout(request):
    return render(request, 'MarketPlace/logout.html')


def dashboard(request):
    return render(request, 'MarketPlace/dashboard.html')


def minha_view(request):
    lojas = Loja.objects.all()  # Query all stores from your database
    return render(request, 'seu_template.html', {'lojas': lojas})


def add_product(request, store_id):
    current_store_id = request.session.get('current_store')
    if current_store_id is None:
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.loja_id = current_store_id
            product.save()

            # Lógica para salvar a imagem na pasta da loja...
            store_folder = os.path.join('media', str(request.user.loja.id))
            os.makedirs(store_folder, exist_ok=True)

            # Move a imagem do produto para a pasta da loja
            product_image_path = os.path.join('media', str(product.imagem))
            new_product_image_path = os.path.join(store_folder, os.path.basename(product_image_path))
            os.rename(product_image_path, new_product_image_path)

            return redirect('product_added_successfully')
    else:
        form = ProductForm()
    return render(request, 'MarketPlace/add_product.html', {'form': form})


def select_store(request):
    store_id = request.POST.get('store_id')
    if store_id:
        request.session['current_store'] = store_id
        return redirect('marketplace:loja', store_id=store_id)
    else:
        # Caso a loja não seja selecionada, redireciona de volta para a página inicial
        return redirect('home')
