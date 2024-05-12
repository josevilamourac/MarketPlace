from django import forms
from .models import Product, UserPerfil, Admin, Loja
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['nome', 'descricao', 'preco', 'quantidade', 'loja']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class LojaForm(forms.ModelForm):
    class Meta:
        model = Loja
        fields = ['telefone', 'endereco', 'descricao', 'imagem']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['user', 'telefone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
