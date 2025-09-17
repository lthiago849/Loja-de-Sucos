from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['name']
        verbose_name = 'Categoria'

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length= 100, verbose_name='Titutlo')
    ingredient  = models.ForeignKey('Ingredient', on_delete=models.PROTECT,related_name='products', verbose_name='Ingrediente')
    quantity = models.PositiveBigIntegerField(default=0, verbose_name='Quantidade em Estoque')
    category = models.ForeignKey(Category, on_delete= models.PROTECT, related_name='products', verbose_name='Categoria')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')  
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')  
    class Meta:
        ordering = ['title']
        verbose_name = 'Produto'

    def __str__(self):
        return self.title

class Cart(models.Model):
    FORMA_PAGAMENTO_CHOICES = [
        ('pix', 'Pix'),
        ('dinheiro', 'Dinheiro'),
        ('debito', 'Cartão de Débito'),
        ('credito', 'Cartão de Crédito'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    finalizado = models.BooleanField(default=False)
    finalizado_em = models.DateTimeField(null=True, blank=True)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Compra #{self.id} - {self.user.username}"
    
    @property
    def total(self):
        return sum(item.product.price * item.quantity for item in self.items.all())
    
    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-finalizado_em']

        
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.title}"
    
class Ingredient(models.Model):
    category_ingredient = models.ForeignKey('CategoryIngredient', on_delete= models.PROTECT, related_name='ingredientes', verbose_name='Categoria')
    quantity = models.DecimalField(max_digits=10,decimal_places=2,default=0.00,verbose_name='Quantidade em Estoque') 
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')  
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')  
    class Meta:
        ordering = ['category_ingredient']
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'

    def __str__(self):
        # Certifique-se de que category_ingredient tenha um campo 'name' ou similar
        return f"{self.category_ingredient.name}"  
        
class CategoryIngredient(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['name']
        verbose_name = 'Categoria de Ingrediente'

    def __str__(self):
        return self.name
    
class Venda(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField()
    forma_pagamento = models.CharField(max_length=30)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venda #{self.id} - {self.user.username if self.user else 'Anônimo'}"


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.title if self.produto else 'Produto removido'}"
