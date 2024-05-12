from django import forms
from .models import Product, UserPerfil, Admin, Loja, Mensagem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['nome', 'descricao', 'preco', 'quantidade', 'loja']

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class UserRegistoForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class UserForm(forms.ModelForm):
    class Meta:
        model = UserPerfil
        fields = ['telefone']  # Removed 'user' from the fields

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class LojaForm(forms.ModelForm):
    class Meta:
        model = Loja
        fields = ['nome','telefone', 'endereco', 'descricao', 'imagem']

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['user', 'telefone']

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['receiver', 'subject', 'content']