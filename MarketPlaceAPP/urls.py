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
    path('loja/<int:store_id>/', views.loja, name='loja'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('loja/<int:store_id>/add_product/', views.add_product, name='add_product'),  # URL para adicionar produtos
    path('home/select_store/', views.select_store, name='select_store'),
    path('add_product/', views.add_product, name='add_product'),
    path('registo_user/', views.registo_user, name='registo_user'),
    path('registo_admin/', views.registo_admin, name='registo_admin'),
    path('registo_loja/', views.registo_loja, name='registo_loja'),

]
