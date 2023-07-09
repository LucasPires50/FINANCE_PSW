from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants

from contas.utils import bucar_contas

from perfil.models import Categoria
from .models import ContaPagar

def definir_contas(request):
    if request.method == 'GET':
        categorias = Categoria .objects.all()
        return render(request, 'definir_contas.html', {'categorias': categorias})
    elif request.method == 'POST':
            titulo = request.POST.get('titulo', None)
            categoria = request.POST.get('categoria', None)
            descricao = request.POST.get('descricao', None)
            dia_pagamento = request.POST.get('dia_pagamento', None)
            valor = request.POST.get('valor', None)
            
            conta = ContaPagar.objects.create(
                titulo = titulo,
                categoria_id = categoria,
                descricao = descricao,
                dia_pagamento = dia_pagamento,
                valor = valor,
            )
            
            messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')
            return redirect(r'/contas/definir_contas')

def ver_contas(request):
    contas_pagas, contas_vencidas, contas_proximas_vencimento, restantes = bucar_contas()
    
    return  render(request, 'ver_contas.html', {
                                            'contas_pagas': contas_pagas, 
                                            'contas_vencidas': contas_vencidas, 
                                            'contas_proximas_vencimento': contas_proximas_vencimento, 
                                            'restantes': restantes
                                        })