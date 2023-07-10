from django.db import models

from perfil.utils import calcula_total
from utils.utils_geral import calula_porcentagem, mes_atual

class Categoria(models.Model):
    
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)
    
    def __str__(self):
        return self.categoria
    
    def total_gasto(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(categoria__id=self.id).filter(data__month=mes_atual()).filter(tipo="S")

        total_valor = calcula_total(valores, "valor")
        
        return total_valor
    
    def cacula_percentual_gasto_por_categoria(self):
        return calula_porcentagem(self.total_gasto(), self.valor_planejamento)

class Conta(models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa economica'),
        ('BR', 'Bradesco'),
    )
    
    tipo_choices = (
        ('pf', 'Pessoa Física'),
        ('pj', 'Caixa Pessoa Jurídica'),
    )
    
    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to="icones")

    def __str__(self):
        return self.apelido
    