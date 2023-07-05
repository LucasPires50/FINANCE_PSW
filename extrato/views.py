from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from extrato.utils import calcular_operação

from perfil.models import Conta, Categoria
from .models import Valores



def novo_valor(request):
    if request.method == 'GET':
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        return render(request, 'novo_valor.html', {'contas': contas, 'categorias': categorias})
    elif request.method == 'POST':
        valor = request.POST.get('valor', None)
        categoria = request.POST.get('categoria', None)
        descricao = request.POST.get('descricao', None)
        data = request.POST.get('data', None)
        conta = request.POST.get('conta', None)
        tipo = request.POST.get('tipo', None)
        
        valores = Valores.objects.create(
            valor=valor,
            categoria_id=categoria,
            descricao=descricao,
            data=data,
            conta_id=conta,
            tipo = tipo,
        )
    
        calcular_operação(valores.conta, float(valores.valor), valores.tipo)
        
    
    # get_tipo_display(), serve para acessar o valor do choice
    messages.add_message(request, constants.SUCCESS, f'{valores.get_tipo_display()} registrada com sucesso!')
    return redirect('/extrato/novo_valor/')