def calcular_operação(conta, valor, tipo):
    if tipo == 'E':
        conta.valor += valor
    elif tipo == 'S':
        conta.valor -= valor
    
    conta.save()