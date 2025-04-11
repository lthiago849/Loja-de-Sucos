from django.urls import path
from .views import IndexView, VendaView, ModeloView, InicioView
from .views import SucoView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('venda/', VendaView.as_view(), name='venda'),
    path('modelo/', ModeloView.as_view(), name='modelo'),
    path('inicio/', InicioView.as_view(), name = 'inicio'),
    path('suco/', SucoView.as_view(), name='suco')
]

