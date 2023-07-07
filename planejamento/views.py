import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from perfil.models import Categoria

def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})

@csrf_exempt
def update_valor_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    novo_valor = json.loads(request).get('novo_valor', None)
    if novo_valor:
        categoria.valor = novo_valor
        categoria.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
