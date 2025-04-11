from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

class VendaView(TemplateView):
    template_name = 'venda.html'

class ModeloView(TemplateView):
    template_name = 'modelo/modelo.html'

class InicioView(TemplateView):
    template_name = 'inicio.html'

class SucoView(TemplateView):
    template_name = 'produtos/suco.html'