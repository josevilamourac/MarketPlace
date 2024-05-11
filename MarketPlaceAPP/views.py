# Create your views here.
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages


from MarketPlace import settings
from .models import Loja, Product


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
    loja = Loja.objects.get(pk=store_id)
    produtos_da_loja = loja.products.all()
    descricao_loja = loja.descricao
    return render(request, 'MarketPlace/loja.html', {'store_id': store_id, 'descricao_loja': descricao_loja, 'produtos_da_loja': produtos_da_loja})


def logout(request):
    return render(request, 'MarketPlace/logout.html')


def dashboard(request):
    return render(request, 'MarketPlace/dashboard.html')


def minha_view(request):
    lojas = Loja.objects.all()  # Query all stores from your database
    return render(request, 'seu_template.html', {'lojas': lojas})


def add_product(request, store_id):
    # Check if store_id is None or not
    if store_id is None:
        return redirect('home')

    # Check if the request method is POST
    if request.method == 'POST':
        # Obtain the store instance
        loja = get_object_or_404(Loja, pk=store_id)

        # Extract data from the POST request
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        quantidade = request.POST.get('quantidade')

        # Create and save the product instance
        product = Product(nome=nome, descricao=descricao, preco=preco, quantidade=quantidade, loja=loja)
        product.save()

        if 'imagem' in request.FILES:
            imagem = request.FILES['imagem']
            # Define o caminho para salvar a imagem
            store_folder = os.path.join(settings.MEDIA_ROOT, 'lojas', str(loja.pk))
            if not os.path.exists(store_folder):
                os.makedirs(store_folder)
            image_path = os.path.join(store_folder, imagem.name)
            # Salva a imagem na pasta
            with open(image_path, 'wb') as f:
                for chunk in imagem.chunks():
                    f.write(chunk)
        # Add logic here to save the image in the store's folder...

        # Redirect to some success URL after processing the form
        mens = "Produto adicionado com sucesso."

        return HttpResponseRedirect(reverse('marketplace:loja', args=[store_id]))
    else:
        # Render the form for GET requests
        return render(request, 'MarketPlace/add_product.html', {'store_id': store_id})


def select_store(request):
    store_id = request.POST.get('store_id')
    if store_id:
        return redirect('marketplace:loja', store_id=store_id)
    else:
        # Caso a loja não seja selecionada, redireciona de volta para a página inicial
        return redirect('home')

def remove_product(request, store_id, product_id):
    # Verifique se store_id e product_id não são None
    if store_id is None or product_id is None:
        return redirect('home')

    # Obtenha a instância da loja e do produto
    loja = get_object_or_404(Loja, pk=store_id)
    product = get_object_or_404(Product, pk=product_id)

    # Verifique se o produto pertence à loja
    if product.loja != loja:
        return redirect('home')  # ou redirecione para uma página de erro

    # Remova o produto
    product.delete()
    messages.success(request, 'Produto removido com sucesso.')
    # Redirecione de volta para a página da loja com uma mensagem de sucesso
    return HttpResponseRedirect(reverse('marketplace:loja', args=[store_id]))
