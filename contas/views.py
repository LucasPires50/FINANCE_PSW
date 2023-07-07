from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants

from datetime import datetime

from perfil.models import Categoria
from .models import ContaPagar, ContaPaga

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
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day
    
    contas = ContaPagar.objects.all()
    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')
    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=(contas_pagas))
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte=DIA_ATUAL+5).filter(dia_pagamento__gt=DIA_ATUAL).exclude(id__in=(contas_pagas))
    restantes = contas.exclude(id__in=(contas_vencidas)).exclude(id__in=(contas_proximas_vencimento)).exclude(id__in=(contas_pagas))
    
    
    return  render(request, 'ver_contas.html', {
                                            'contas_pagas': contas_pagas, 
                                            'contas_vencidas': contas_vencidas, 
                                            'contas_proximas_vencimento': contas_proximas_vencimento, 
                                            'restantes': restantes
                                        })