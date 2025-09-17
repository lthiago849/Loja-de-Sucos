from django.shortcuts import render, redirect,  get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

class VendaView(TemplateView):
    template_name = 'venda.html'

class ModeloView(TemplateView):
    template_name = 'modelo/modelo.html'

class InicioView(TemplateView):
    template_name = 'inicio.html'

class GeladosView(TemplateView):
    template_name = 'produtos/gelados/gelados.html'

class RelatorioView(TemplateView):
    template_name = 'relatorio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        hoje = timezone.now().date()
        periodo = self.request.GET.get('periodo', 'hoje')
        
        # Base das vendas
        vendas = Venda.objects.all()
        
        # Aplicar filtros de período
        if periodo == 'hoje':
            vendas = vendas.filter(data__date=hoje)
            titulo_periodo = "Hoje"
        elif periodo == 'semana':
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            vendas = vendas.filter(data__date__gte=inicio_semana)
            titulo_periodo = "Esta Semana"
        elif periodo == 'mes':
            vendas = vendas.filter(data__year=hoje.year, data__month=hoje.month)
            titulo_periodo = "Este Mês"
        else:
            titulo_periodo = "Todas as Vendas"
        
        # Estatísticas gerais
        total_vendido = vendas.aggregate(total=Sum('valor_total'))['total'] or 0
        total_vendas = vendas.count()
        
        # Relatório por forma de pagamento
        formas_pagamento = vendas.values('forma_pagamento').annotate(
            total=Sum('valor_total'),
            quantidade=Count('id')
        ).order_by('-total')
        
        # Calcular percentuais
        for forma in formas_pagamento:
            if total_vendido > 0:
                forma['percentual'] = (forma['total'] / total_vendido) * 100
            else:
                forma['percentual'] = 0
            
            # Nome amigável da forma de pagamento
            forma_nome = {
                'pix': 'Pix',
                'dinheiro': 'Dinheiro',
                'debito': 'Cartão de Débito',
                'credito': 'Cartão de Crédito'
            }.get(forma['forma_pagamento'], forma['forma_pagamento'])
            forma['nome'] = forma_nome
        
        context.update({
            'vendas': vendas.order_by('-data'),
            'total_vendido': total_vendido,
            'total_vendas': total_vendas,
            'formas_pagamento': formas_pagamento,
            'periodo': periodo,
            'titulo_periodo': titulo_periodo,
        })
        
        return context

def listar_sucos(request):
    sucos = Product.objects.filter(category__name='Suco', is_active = True )
    return render(request, 'produtos/suco.html', {'sucos':sucos})

def listar_sucos_producao(request):
    sucos_producao = Product.objects.filter(category__name='Suco', is_active=True)
    
    try:
        # Busca TODOS os ingredientes da categoria Açúcar e soma as quantidades
        ingredientes_acucar = Ingredient.objects.filter(
            category_ingredient__name='Açucar'
        )
        acucar_disponivel = sum(ing.quantity for ing in ingredientes_acucar)
        
    except Exception as e:
        print(f"Erro ao buscar açúcar: {str(e)}")
        acucar_disponivel = 0

    return render(request, 'producao/producao_suco.html', {
        'sucos_producao': sucos_producao,
        'acucar_disponivel': acucar_disponivel
    })
def listar_picole(request):
    picole= Product.objects.filter(category__name = 'Picole', is_active =  True)
    return render(request, 'produtos/gelados/picole.html', {'picoles': picole})

def listar_moreninha(request):
    moreninha= Product.objects.filter(category__name = 'Moreninha', is_active =  True)
    return render(request, 'produtos/gelados/moreninha.html', {'moreninhas': moreninha})

def listar_cremosinho(request):
    cremosinho= Product.objects.filter(category__name = 'Cremosinho', is_active =  True)
    return render(request, 'produtos/gelados/cremosinho.html', {'cremosinhos': cremosinho})


def adicionar_ao_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        quantidade = int(request.POST.get('quantidade', 1))
        produto = get_object_or_404(Product, id=produto_id)

        cart, created = Cart.objects.get_or_create(user=request.user, finalizado=False)
        item, created = CartItem.objects.get_or_create(cart=cart, product=produto)
        if not created:
            item.quantity += quantidade
        else:
            item.quantity = quantidade
        item.save()

    return redirect('ver_carrinho')

def ver_carrinho(request):
    cart, created = Cart.objects.get_or_create(user=request.user, finalizado=False)   
    itens_queryset = cart.items.select_related('product')

    itens = []
    total = 0

    for item in itens_queryset:
        subtotal = item.product.price * item.quantity
        total += subtotal
        itens.append({
            'id': item.id,
            'product': item.product,
            'quantity': item.quantity,
            'subtotal': subtotal
        })

    return render(request, 'ver_carrinho.html', {'cart': cart, 'itens': itens, 'total': total})

def remover_do_carrinho(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('ver_carrinho')


def atualizar_carrinho(request, item_id):
    if request.method == 'POST':
        nova_quantidade = int(request.POST.get('quantidade', 1))
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        if nova_quantidade > 0:
            item.quantity = nova_quantidade
            item.save()
        else:
            item.delete()  # Se quantidade for 0, remove

    return redirect('ver_carrinho')


# class InicioView(LoginRequiredMixin, TemplateView):
#     template_name = "inicio.html"
#     login_url = 'accounts/login/'  # nome da URL da sua tela de login

from .forms import IngredienteForm

def sua_view(request):
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            # Você pode redirecionar para a mesma página, ou outra
            return redirect('sua_view')
    else:
        form = IngredienteForm()

    return render(request, 'producao_suco.html', {'form': form})


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from .models import Product, Ingredient
from decimal import Decimal
@require_POST
@csrf_exempt
def adicionar_producao(request):
    try:
        produto_id = request.POST.get('produto_id')
        quantidade = int(request.POST.get('quantidade', 0))
        polpa = Decimal(request.POST.get('polpa', 0).replace(',', '.'))
        acucar = Decimal(request.POST.get('acucar', 0).replace(',', '.'))
        
        produto = Product.objects.get(id=produto_id)
        polpa_ingrediente = produto.ingredient
        
        # Busca TODOS os ingredientes de açúcar
        ingredientes_acucar = Ingredient.objects.filter(
            category_ingredient__name='Açucar'
        )
        
        # Calcula o total disponível
        total_acucar_disponivel = sum(ing.quantity for ing in ingredientes_acucar)
        
        if acucar > total_acucar_disponivel:
            return JsonResponse({'success': False, 'message': 'Estoque total de açúcar insuficiente'})
        
        # Atualiza a polpa (ingrediente específico do produto)
        polpa_ingrediente.quantity -= polpa
        polpa_ingrediente.save()
        
        # Atualiza o açúcar (distribui a redução entre os ingredientes)
        acucar_restante = acucar
        for ing in ingredientes_acucar:
            if acucar_restante <= 0:
                break
            if ing.quantity > 0:
                reducao = min(ing.quantity, acucar_restante)
                ing.quantity -= reducao
                acucar_restante -= reducao
                ing.save()
        
        produto.quantity += quantidade
        produto.save()
        
        # Calcula os novos totais
        novo_total_acucar = sum(ing.quantity for ing in Ingredient.objects.filter(
            category_ingredient__name='Açucar'
        ))
        
        return JsonResponse({
            'success': True,
            'message': 'Produção registrada com sucesso!',
            'novo_estoque': produto.quantity,
            'polpa_restante': str(polpa_ingrediente.quantity.quantize(Decimal('0.00'))),
            'acucar_restante': str(novo_total_acucar.quantize(Decimal('0.00')))
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
def get_total_ingrediente_por_categoria(nome_categoria):
    ingredientes = Ingredient.objects.filter(
        category_ingredient__name=nome_categoria
    )
    return sum(ing.quantity for ing in ingredientes)

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from decimal import Decimal

from .models import Venda, ItemVenda  # importe os modelos novos
@transaction.atomic
def finalizar_compra(request):
    if request.method == 'POST':
        try:
            # Buscar carrinho não finalizado
            carrinho = Cart.objects.filter(user=request.user, finalizado=False).first()
            
            if not carrinho:
                # Se não tem carrinho, criar um novo
                carrinho = Cart.objects.create(user=request.user, finalizado=False)
            
            # Verificar se tem itens
            if not carrinho.items.exists():
                messages.error(request, 'Seu carrinho está vazio!')
                return redirect('ver_carrinho')
            
            forma_pagamento = request.POST.get('forma_pagamento')
            valor_total = Decimal(request.POST.get('valor_total', '0').replace(',', '.'))
            
            # Verificação e atualização do estoque
            for item in carrinho.items.all():
                produto = item.product
                if produto.quantity < item.quantity:
                    messages.error(request, f'Estoque insuficiente para {produto.title}. Disponível: {produto.quantity}')
                    return redirect('ver_carrinho')
                produto.quantity -= item.quantity
                produto.save()
            
            # Marcar o carrinho como finalizado
            carrinho.finalizado = True
            carrinho.finalizado_em = timezone.now()
            carrinho.forma_pagamento = forma_pagamento
            carrinho.valor_total = valor_total
            carrinho.save()
            
            # Criar a venda
            venda = Venda.objects.create(
                user=request.user,
                data=carrinho.finalizado_em,
                forma_pagamento=forma_pagamento,
                valor_total=valor_total
            )
            
            # Criar os itens da venda
            for item in carrinho.items.all():
                ItemVenda.objects.create(
                    venda=venda,
                    produto=item.product,
                    quantidade=item.quantity,
                    preco_unitario=item.product.price
                )
            
            messages.success(request, 'Compra finalizada com sucesso!')
            return redirect('relatorio')
            
        except Exception as e:
            messages.error(request, f'Ocorreu um erro: {str(e)}')
            return redirect('ver_carrinho')
    
    return redirect('ver_carrinho')

from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

def relatorio_vendas(request):
    hoje = timezone.now().date()
    periodo = request.GET.get('periodo', 'hoje')

    # Se for staff/admin, mostra tudo; senão, só do usuário logado
    if request.user.is_staff:
        vendas = Venda.objects.all()
    else:
        vendas = Venda.objects.filter(user=request.user)

    # Filtros de período
    # Filtros de período  
    if periodo == 'hoje':
        vendas = vendas.filter(data__date=hoje)
    elif periodo == 'todos':  # ← ADICIONE ESTA OPÇÃO
        pass  # Não filtra, mostra todas
    elif periodo == 'semana':
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        vendas = vendas.filter(data__date__gte=inicio_semana)
        titulo_periodo = "Esta Semana"
    elif periodo == 'mes':
        vendas = vendas.filter(data__year=hoje.year, data__month=hoje.month)
        titulo_periodo = "Este Mês"
    else:
        titulo_periodo = "Todos os Períodos"

    total_vendido = vendas.aggregate(total=Sum('valor_total'))['total'] or 0
    total_vendas = vendas.count()
    formas_pagamento = vendas.values('forma_pagamento').annotate(
        total=Sum('valor_total'),
        quantidade=Count('id')
    )

    context = {
        'vendas': vendas,
        'total_vendido': total_vendido,
        'total_vendas': total_vendas,
        'formas_pagamento': formas_pagamento,
        'periodo': periodo,
        'titulo_periodo': titulo_periodo,
        'modo_admin': request.user.is_staff,
    }

    return render(request, 'relatorio.html', context)

from django.shortcuts import render
from django.http import HttpResponse

def minha_view_personalizada(request):
    # Lógica para a ação personalizada
    return HttpResponse("Ação personalizada executada!")
