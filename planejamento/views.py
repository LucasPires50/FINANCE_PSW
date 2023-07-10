import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.messages import constants
from extrato.models import Valores

from perfil.models import Categoria
from perfil.utils import calcula_total
from utils.utils_geral import calula_porcentagem

def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})

@csrf_exempt
def update_valor_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    novo_valor = json.load(request).get('novo_valor', None)
    if novo_valor:
        categoria.valor_planejamento = novo_valor
        categoria.save()
    return JsonResponse({'status': 'success'})

def ver_planejamento(request):
    categorias = Categoria.objects.all()

    valores = Valores.objects.all()

    total_gasto = calcula_total(valores, "valor")
    
    total_planejamento = calcula_total(categorias, "valor_planejamento")
    
    calcular_porcentagem_total_gatos = calula_porcentagem(total_gasto, total_planejamento)
    
    return render(request, 'ver_planejamento.html', {'categorias': categorias, 
                                                     "total_gasto": total_gasto, 
                                                     "total_planejamento": total_planejamento, 
                                                     "calcular_porcentagem_total_gatos": calcular_porcentagem_total_gatos})