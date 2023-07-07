
from django.db.models import Sum

def calcula_total(obj, campo):
    total_contas = obj.aggregate(soma=Sum(campo))['soma']
    if not total_contas:
        total_contas = 0
    return total_contas