from django.shortcuts import render, redirect,  get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem
from django.contrib.auth.mixins import LoginRequiredMixin

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
# class SucoView(TemplateView):
#     template_name = 'produtos/suco.html'
class ProducaoView(TemplateView):
    template_name = 'producao/producao.html'

class CompraView(TemplateView):
    template_name  = 'producao/compra.html'

# class ProducaoSucoView(TemplateView):
#     template_name = 'producao/producao_suco.html'


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


@login_required
def adicionar_ao_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        quantidade = int(request.POST.get('quantidade', 1))
        produto = get_object_or_404(Product, id=produto_id)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(cart=cart, product=produto)
        if not created:
            item.quantity += quantidade
        else:
            item.quantity = quantidade
        item.save()

    return redirect('ver_carrinho')

@login_required
def ver_carrinho(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
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

@login_required
def remover_do_carrinho(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('ver_carrinho')


@login_required
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