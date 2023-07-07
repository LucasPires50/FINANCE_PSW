from django.contrib import admin
from .models import Conta, Categoria

# Registrar na area administativa
admin.site.register(Conta)
admin.site.register(Categoria)
