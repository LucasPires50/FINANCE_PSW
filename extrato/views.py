import os

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from extrato.utils import calcular_operação
from django.template.loader import render_to_string
from django.conf import settings
from django.http import FileResponse


from datetime import datetime, timedelta
from weasyprint import HTML
from io import BytesIO

from perfil.models import Conta, Categoria
from utils.utils_geral import mes_atual
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

def view_extrato(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    valores = Valores.objects.filter(data__month=mes_atual())
    conta_get = request.GET.get('conta', None)
    categoria_get = request.GET.get('categoria', None)
    periodo_get = request.GET.get('periodo', None)
    
    if conta_get:
        valores = valores.filter(conta_id=conta_get)
    if categoria_get:
        valores = valores.filter(categoria_id=categoria_get)
    if periodo_get:
            ultimos_sete_dias = datetime.now().date() - timedelta(days=7)
            valores = valores.filter(data__range=(ultimos_sete_dias, datetime.now().date()))
    
    
    #TODO: Fazer botão para limpar os filtros
    return render(request, 'view_extrato.html', {"valores":valores, "categorias":categorias, "contas":contas})

def exportar_pdf(request):
    valores = Valores.objects.filter(data__month=mes_atual())
    
    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    template_render = render_to_string(path_template, {'valores':valores})
    
    # Salva o objeto em memória
    path_output = BytesIO()
    HTML(string=template_render).write_pdf(path_output)
    path_output.seek(0)
    
    return FileResponse(path_output, filename="extrato.pdf")