
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants

from datetime import datetime

from .models import Conta, Categoria
from extrato.models import Valores
from .utils import calcula_total, calcula_equilibiro_financeiro

def home(request):
    contas = Conta.objects.all()
    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo="E")
    saidas = valores.filter(tipo="S")
    
    total_contas = calcula_total(contas, 'valor')
    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')
    
    percental_gastos_essencias, percental_gastos_nao_essencias = calcula_equilibiro_financeiro()
    
    return render(request, 'home.html', {'contas': contas, 'total_contas':total_contas, 'total_entradas':total_entradas, 'total_saidas':total_saidas, 'percental_gastos_essencias':int(percental_gastos_essencias), 'percental_gastos_nao_essencias':int(percental_gastos_nao_essencias)})

def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    total_contas = calcula_total(contas, 'valor')
    
    return render(request, 'gerenciar.html', {'contas': contas, 'total_contas':total_contas, 'categorias':categorias})

def cadastrar_banco(request):
    # Sempre que for para pegar dados normais é atraves do post
    apelido = request.POST.get('apelido', None)
    banco = request.POST.get('banco', None)
    tipo = request.POST.get('tipo', None)
    valor = request.POST.get('valor', None)
    # Para pegar arquivo tem que usar o files
    icone = request.FILES.get('icone', None)
    
    if not apelido or not valor:
        # Mandar a menssagem de erro para o front
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')
    
    conta = Conta(
        apelido=apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )
    
    conta.save()
    
    # Mandar a menssagem de sucesso para o front
    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')
    return redirect('/perfil/gerenciar/')

def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    
    # Mandar a menssagem de sucesso para o front
    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso!')
    return redirect('/perfil/gerenciar/')

def cadastrar_categoria(request):
    nome = request.POST.get('categoria', None)
    essencial = bool(request.POST.get('essencial', None))
    
    if not nome:
        # Mandar a menssagem de erro para o front
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')
    
    if not isinstance(essencial, bool):
        messages.add_message(request, constants.ERROR, 'Valor inválido')
        return redirect('/perfil/gerenciar/')

    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')

def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()
    
    messages.add_message(request, constants.SUCCESS, 'Categoria atualizada com sucesso')
    return redirect('/perfil/gerenciar/')

def dashboard(request):
    dados  = {}
    categorias = Categoria.objects.all()
    
    for categoria in categorias:
        valores = Valores.objects.filter(categoria=categoria)
        total_gasto = calcula_total(valores, 'valor')
        dados[categoria.categoria] = total_gasto
    
    print(dados)

    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 
                                              'values': list(dados.values())})