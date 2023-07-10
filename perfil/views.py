
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants

from contas.utils import bucar_contas
from utils.utils_geral import mes_atual

from .models import Conta, Categoria
from extrato.models import Valores
from .utils import calcula_total, calcula_equilibiro_financeiro

def home(request):
    contas = Conta.objects.all()
    
    contas_pagas, contas_vencidas, contas_proximas_vencimento, restantes = bucar_contas()
    
    valores = Valores.objects.filter(data__month=mes_atual())
    entradas = valores.filter(tipo="E")
    saidas = valores.filter(tipo="S")
    
    total_contas = calcula_total(contas, 'valor')
    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')
    total_livre = total_entradas - total_saidas
    
    percental_gastos_essencias, percental_gastos_nao_essencias = calcula_equilibiro_financeiro()
    
    print(percental_gastos_essencias, percental_gastos_nao_essencias)
    
    return render(request, 'home.html', {'contas': contas, 
                                         'total_contas':total_contas, 
                                         'total_entradas':total_entradas, 
                                         'total_saidas':total_saidas, 
                                         'percental_gastos_essencias':percental_gastos_essencias, 
                                         'percental_gastos_nao_essencias':percental_gastos_nao_essencias, 
                                         'total_livre':total_livre, 
                                         'contas_vencidas':contas_vencidas.count(), 
                                         'contas_proximas_vencimento':contas_proximas_vencimento.count()})

def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    total_contas = calcula_total(contas, 'valor')
    
    return render(request, 'gerenciar.html', {'contas': contas, 
                                              'total_contas':total_contas, 
                                              'categorias':categorias})

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
    
    conta = Conta.objects.create(
        apelido=apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )
    
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

    categoria = Categoria.objects.create(
        categoria=nome,
        essencial=essencial
    )

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