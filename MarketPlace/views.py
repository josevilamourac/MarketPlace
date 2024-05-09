from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return HttpResponse("Pagina de entrada da app votacao.")

def main(request):
    return

def home(request):
    return render (request, 'MarketPlace/home.html')
