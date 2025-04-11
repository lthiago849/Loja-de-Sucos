from django.urls import path
from .views import IndexView, TesteView, ModeloView, InicioView

urlpatterns = [
    path('', IndexView.as_view(), name='venda'),
    path('teste/', TesteView.as_view(), name='teste'),
    path('modelo/', ModeloView.as_view(), name='modelo'),
    path('inicio/', InicioView.as_view(), name = 'inicio'),
]

