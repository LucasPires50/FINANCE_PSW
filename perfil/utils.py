
from django.db.models import Sum

def calcula_total(obj, campo):
    total_contas = obj.aggregate(soma=Sum(campo))['soma']
    return total_contas