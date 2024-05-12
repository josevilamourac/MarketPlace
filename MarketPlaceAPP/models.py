from django.db import models
from django.contrib.auth.models import User

class Loja(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='loja')
    nome = models.CharField(default="Sem Nome", max_length=50)
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='images/', null=True, blank=True)  # Campo de imagem do produto

    def __str__(self):
        return self.user.username

class Product(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.DecimalField(max_digits=10, decimal_places=0)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.nome

class UserPerfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15)
    messages_sent = models.ManyToManyField('Mensagem', related_name='senders')
    messages_received = models.ManyToManyField('Mensagem', related_name='receivers')
    products_bought = models.ManyToManyField('Product', related_name='buyers')
    is_manager = models.BooleanField(default=False)  # Campo para representar se é um gerente
    is_admin = models.BooleanField(default=False)  # Campo para representar se é um administrador

    def __str__(self):
        return self.user.username

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class Mensagem(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.subject}"
