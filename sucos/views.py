from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

class TesteView(TemplateView):
    template_name = 'teste.html'

class ModeloView(TemplateView):
    template_name = 'modelo/modelo.html'

class InicioView(TemplateView):
    template_name = 'inicio.html'

