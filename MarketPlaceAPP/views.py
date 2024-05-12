# Create your views here.
import os
from django.core.files.storage import FileSystemStorage
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
from .forms import ProductForm
from .models import Loja, UserPerfil
from MarketPlace import settings
from .models import Loja, Product
from django.contrib.auth.decorators import login_required, user_passes_test
import glob

def index(request):
    return home(request)


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
            return render(request, 'marketplace/login.html',
                          {'error_message': 'Credenciais inválidas. Por favor, tente novamente.'})

    return render(request, 'marketplace/login.html')


def contact(request):
    return render(request, 'MarketPlace/contact.html')


@login_required
def perfil(request):
    return render(request, 'MarketPlace/perfil.html')


@login_required
def carrinho(request):
    return render(request, 'MarketPlace/carrinho.html')


@login_required
def loja(request, store_id):
    loja = Loja.objects.get(pk=store_id)
    loja_nome = loja.nome
    produtos_da_loja = loja.products.all()
    descricao_loja = loja.descricao
    user_loja = loja.user
    return render(request, 'MarketPlace/loja.html',
                  {'loja_nome': loja_nome, 'store_id': store_id, 'descricao_loja': descricao_loja,
                   'produtos_da_loja': produtos_da_loja,
                   'user_loja': user_loja})


@login_required
def dashboard(request):
    return render(request, 'MarketPlace/dashboard.html')


def minha_view(request):
    lojas = Loja.objects.all()  # Query all stores from your database
    return render(request, 'seu_template.html', {'lojas': lojas})


@login_required
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


@login_required
def select_store(request):
    store_id = request.POST.get('store_id')
    if store_id:
        return redirect('marketplace:loja', store_id=store_id)
    else:
        # Caso a loja não seja selecionada, redireciona de volta para a página inicial
        return redirect('home')


@login_required
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
        # Obtenha os dados do formulário do request.POST
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        # Verifique se as senhas coincidem
        if password1 != password2:
            # Retorne uma mensagem de erro se as senhas não coincidirem
            return render(request, 'MarketPlace/registo_user.html', {'error_message': 'As senhas não coincidem.'})

        # Verifique se já existe um usuário com o mesmo nome de usuário ou e-mail
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            # Retorne uma mensagem de erro se o usuário ou e-mail já estiverem em uso
            return render(request, 'MarketPlace/registo_user.html',
                          {'error_message': 'Nome de usuário ou e-mail já em uso.'})

        # Crie o usuário
        user = User.objects.create_user(username=username, email=email, password=password1)

        # Crie o perfil do usuário
        user_profile = UserPerfil.objects.create(user=user)

        # Autentique o usuário recém-criado e faça o login
        user = authenticate(username=username, password=password1)
        login(request, user)

        # Redirecione para a página inicial
        return redirect('marketplace:home')

    else:
        # Se o método for GET, exiba o formulário vazio
        return render(request, 'MarketPlace/registo_user.html')


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
                    nome = request.POST.get('nome')
                    descricao = request.POST.get('descricao')
                    imagem = request.FILES.get('imagem')
                    telefone = request.POST.get('telefone')  # Use request.POST.get() for non-file fields
                    endereco = request.POST.get('endereco')  # Use request.POST.get() for non-file fields
                    if request.FILES.get('imagem') is not None:
                        imagem = request.FILES.get('imagem')
                        fs = FileSystemStorage()
                        filename = "loja_" + nome
                        filename = fs.save(filename, imagem)
                        uploaded_file_url = fs.url(filename)
                        file_url = render_file(request)
                    print("Encontrou perfil e vai criar loja!")

                    loja = Loja.objects.create(
                        nome=nome,
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
            nome = request.POST.get('nome')
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')
            telefone = request.POST.get('telefone')
            endereco = request.POST.get('endereco')
            descricao = request.POST.get('descricao')
            imagem = request.FILES.get('imagem')  # Para campos de arquivo, use request.FILES

            # Verificar se o usuário já possui uma loja
            if Loja.objects.filter(user__username=username).exists():
                messages.error(request, 'Este usuário já possui uma loja.')
                return redirect('MarketPlace:registo_loja')

            # Crie o usuário
            user = User.objects.create_user(username=username, email=email, password=password1)

            perfil = UserPerfil.objects.create(user=user, telefone=telefone, is_manager=True)
            loja = Loja.objects.create(user=user, nome=nome, telefone=telefone, endereco=endereco, descricao=descricao,
                                       imagem=imagem)

            # Faça a autenticação e redirecione
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login efetuado com sucesso!.')
                return redirect('marketplace:home')

        return render(request, 'MarketPlace/registo_loja.html')


@login_required
def logout(request):
    auth_logout(request)
    # Redirecionar para a página de login ou para qualquer outra página que desejar
    return redirect('marketplace:home')


@login_required
def remover_loja(request, loja_id):
    loja = get_object_or_404(Loja, id=loja_id)

    # Verifique se o usuário logado é o proprietário da loja
    if request.user == loja.user or request.user.is_superuser:
        # Remova a loja
        loja.delete()
        messages.success(request, 'Loja removida com sucesso!.')

        return redirect('marketplace:home')
    else:
        # Se o usuário não for o proprietário da loja, redirecione para alguma página de erro ou aviso
        messages.success(request, 'Nao tem permissoes para tal!.')
        return redirect('marketplace:home')


@login_required
def render_file(request):
    file_pattern = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_*.*")
    matching_files = glob.glob(file_pattern)

    if matching_files:
        file_path = matching_files[0]
        file_name = os.path.basename(file_path)
        file_url = os.path.join(settings.MEDIA_URL, file_name)
    else:
        file_url = None

    return file_url


@login_required()
def fazer_upload(request):
    if request.method == 'POST' and request.FILES.get('myfile') is not None:
        user = request.user
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = user.username + "_" + myfile.name
        filename = fs.save(filename, myfile)
        uploaded_file_url = fs.url(filename)
        file_url = render_file(request)
        return render(request, 'votacao/fazer_upload.html',
                      {'uploaded_file_url': uploaded_file_url, 'file_url': file_url})
    file_url = render_file(request)
    return render(request, 'votacao/fazer_upload.html', {'file_url': file_url})
