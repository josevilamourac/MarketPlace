# Create your views here.
import os

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
import os
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import UserForm, UserRegistoForm, AdminForm, LojaForm
from .models import Item, Carrinho, Compra



from .forms import ProductForm
from .models import Loja, UserPerfil

from MarketPlace import settings
from .models import Loja, Product


def index(request):
    return HttpResponse("Pagina de entrada da app votacao.")


def home(request):
    lojas = Loja.objects.all()  # Recupera todos os objetos de loja do banco de dados
    return render(request, 'MarketPlace/home.html', {'lojas': lojas})



def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('marketplace:home')
        else:
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
            return render(request, 'marketplace/login.html', {'error_message': 'Credenciais inválidas. Por favor, tente novamente.'})

    return render(request, 'marketplace/login.html')

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
    user_loja = loja.user
    return render(request, 'MarketPlace/loja.html', {'store_id': store_id, 'descricao_loja': descricao_loja, 'produtos_da_loja': produtos_da_loja, 'user_loja': user_loja})





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
    if request.user.is_authenticated:
        # Verifique se o perfil do usuário existe
        if hasattr(request.user, 'userperfil'):
            # Verifique se o usuário é um gerente
            if request.user.userperfil.is_manager:
                if Loja.objects.filter(user=request.user).exists():
                    messages.error(request, 'Este usuário já possui uma loja.')
                    return redirect('marketplace:registo_loja')
                if request.method == 'POST':
                    descricao = request.POST.get('descricao')
                    imagem = request.FILES.get('imagem')
                    telefone = request.POST.get('telefone')  # Use request.POST.get() for non-file fields
                    endereco = request.POST.get('endereco')  # Use request.POST.get() for non-file fields

                    print("Encontrou perfil e vai criar loja!")

                    loja = Loja.objects.create(
                        telefone=telefone,
                        endereco=endereco,
                        descricao=descricao,
                        user=request.user,
                        imagem=imagem
                    )
                    messages.success(request, 'Loja criada!.')
                    return redirect('marketplace:home')


                return render(request, 'MarketPlace/registo_loja.html')



            else:
                # O usuário não é um gerente
                # Redirecione ou retorne uma resposta proibida
                return HttpResponseForbidden("Nao tem permissoes!.")
        else:
            # O perfil do usuário não está configurado
            # Redirecione ou retorne uma resposta proibida
            return HttpResponseForbidden("Nao tem permissoes!")
    else:
        # O usuário não está autenticado
        # Redirecione ou retorne uma resposta proibida
        if request.method == 'POST':
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')
            telefone = request.POST.get('telefone')
            endereco = request.POST.get('endereco')
            descricao = request.POST.get('descricao')
            saldo = request.POST.get('saldo')

            imagem = request.FILES.get('imagem')  # Para campos de arquivo, use request.FILES

            # Verificar se o usuário já possui uma loja
            if Loja.objects.filter(user__username=username).exists():
                messages.error(request, 'Este usuário já possui uma loja.')
                return redirect('MarketPlace:registo_loja')

            # Crie o usuário
            user = User.objects.create_user(username=username, email=email, password=password1)

            perfil = UserPerfil.objects.create(user=user, telefone=telefone, is_manager=True, saldo=saldo)
            loja = Loja.objects.create(user=user, telefone=telefone, endereco=endereco, descricao=descricao,
                                       imagem=imagem)

            # Faça a autenticação e redirecione
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login efetuado com sucesso!.')
                return redirect('marketplace:home')

        return render(request, 'MarketPlace/registo_loja.html')












def logout(request):
    auth_logout(request)
    # Redirecionar para a página de login ou para qualquer outra página que desejar
    return redirect('marketplace:home')


def remover_loja(request, loja_id):
    loja = get_object_or_404(Loja, id=loja_id)

    # Verifique se o usuário logado é o proprietário da loja
    if request.user == loja.user:
        # Remova a loja
        loja.delete()
        messages.success(request, 'Loja removida com sucesso!.')

        return redirect('marketplace:home')
    else:
        # Se o usuário não for o proprietário da loja, redirecione para alguma página de erro ou aviso
        messages.success(request, 'Nao tem permissoes para tal!.')
        return redirect('marketplace:home')

def adicionar_carrinho(request, item_id):
    if request.method == 'POST':
        produto = get_object_or_404(Product, id=item_id)
        carrinho, created = Carrinho.objects.get_or_create(user=request.user)
        carrinho.itens.add(produto)
        messages.success(request, 'Adicionado ao carrinho!')
        # Redireciona para a página da loja
        return redirect('marketplace:loja', store_id=produto.loja.id)
    else:
        produto = get_object_or_404(Product, id=item_id)

        return redirect('marketplace:loja', store_id=produto.loja.id)

def fazer_compra(user, request):
    carrinho = get_object_or_404(Carrinho, user=user)
    total = sum(item.preco for item in carrinho.itens.all())
    user_profile = request.user.userperfil  # Obtém o perfil do usuário atual
    saldo = user_profile.saldo  # Obtém o saldo do perfil do usuário
    if saldo >= total:
        for item in carrinho.itens.all():
            Compra.objects.create(user=user, item=item, quantidade=1)
        user_profile.saldo -= total  # Deduz o total do saldo do perfil do usuário
        user_profile.save()  # Salva as alterações no perfil do usuário
        carrinho.itens.clear()
        return True
    else:
        return False