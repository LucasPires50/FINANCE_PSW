from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def gerenciar(request):
    return render(request, 'gerenciar.html')

def cadastrar_banco(request):
    # Sempre que for para pegar dados normais é atraves do post
    apelido = request.POST.get('apelido', None)
    banco = request.POST.get('banco', None)
    tipo = request.POST.get('tipo', None)
    valor = request.POST.get('valor', None)
    apelido = request.POST.get('apelido', None)
    # Para pegar arquivo tem que usar o files
    icone = request.FILES.get('icone', None)
    
    return render(request, 'cadastrar_banco.html')