
from datetime import datetime

from contas.models import ContaPagar, ContaPaga
from utils.utils_geral import dia_atual, mes_atual

def bucar_contas():
    MES_ATUAL = mes_atual()
    DIA_ATUAL = dia_atual()
    
    contas = ContaPagar.objects.all()
    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')
    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=(contas_pagas))
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte=DIA_ATUAL+5).filter(dia_pagamento__gt=DIA_ATUAL).exclude(id__in=(contas_pagas))
    restantes = contas.exclude(id__in=(contas_vencidas)).exclude(id__in=(contas_proximas_vencimento)).exclude(id__in=(contas_pagas))
    
    return contas_pagas, contas_vencidas, contas_proximas_vencimento, restantes