from django.urls import path
from .views import IndexView, VendaView, ModeloView, InicioView, GeladosView, ProducaoView, CompraView
# from .views import SucoView
from .views import listar_sucos,listar_picole,listar_moreninha,listar_cremosinho, listar_sucos_producao, adicionar_producao
from .views import adicionar_ao_carrinho,  ver_carrinho,  remover_do_carrinho, atualizar_carrinho


urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('venda/', VendaView.as_view(), name='venda'),
    path('modelo/', ModeloView.as_view(), name='modelo'),
    path('', InicioView.as_view(), name = 'inicio'),
    path('gelados/', GeladosView.as_view(), name = 'gelados'),
    path('producao/', ProducaoView.as_view(), name = 'producao'),
    path('compra/', CompraView.as_view(), name = 'compra'),


    # path('suco/', SucoView.as_view(), name='suco'),


    path('sucos/', listar_sucos, name='sucos'),
    path('sucos-producao/', listar_sucos_producao, name='sucos-producao'),

    path('adicionar_producao/', adicionar_producao, name='adicionar_producao'),

    path('picole/', listar_picole, name='picole'),
    path('moreninha/', listar_moreninha, name='moreninha'),
    path('cremosinho/', listar_cremosinho, name='cremosinho'),

    path('adicionar-carrinho/', adicionar_ao_carrinho, name='adicionar_carrinho'),

    path('carrinho/',ver_carrinho, name='ver_carrinho'),
    path('carrinho/remover/<int:item_id>/', remover_do_carrinho, name='remover_do_carrinho'),
    path('carrinho/atualizar/<int:item_id>/', atualizar_carrinho, name='atualizar_carrinho'),
]
