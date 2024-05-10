from django.urls import include, path
from django.contrib import admin
from . import views


app_name = 'MarketPlaceAPP'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('contact/', views.contact, name='contact'),
    path('perfil/', views.perfil, name='perfil'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('loja/', views.loja, name='loja'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
