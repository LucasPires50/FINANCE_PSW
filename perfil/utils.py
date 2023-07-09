
from django.db.models import Sum

from datetime import datetime


def calcula_total(obj, campo):
    total_contas = obj.aggregate(soma=Sum(campo))['soma']
    if not total_contas:
        total_contas = 0
    return total_contas

def calcula_equilibiro_financeiro():
    # Para evitar importação circular
    from extrato.models import Valores
    gastos_essencias = Valores.objects.filter(data__month=datetime.now().month).filter(tipo="S").filter(categoria__essencial=True)
    gastos_nao_essencias = Valores.objects.filter(data__month=datetime.now().month).filter(tipo="S").filter(categoria__essencial=False)
    
    total_gastos_essencias = calcula_total(gastos_essencias, 'valor')
    total_gastos_nao_essencias = calcula_total(gastos_nao_essencias, 'valor')
    
    total = total_gastos_essencias + total_gastos_nao_essencias
    try:
        percentual_gastos_essencias = (total_gastos_essencias * 100) / total
        percentual_gastos_nao_essencias = (total_gastos_nao_essencias * 100) / total
        return percentual_gastos_essencias, percentual_gastos_nao_essencias
    except :
        return 0, 0