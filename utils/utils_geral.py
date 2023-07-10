from datetime import datetime

def mes_atual():
    return datetime.now().month

def dia_atual():
    return datetime.now().day

def calula_porcentagem(porcentagem, valor):
    return int((porcentagem * 100) / valor)
    