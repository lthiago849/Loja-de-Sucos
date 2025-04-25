import csv
from django.contrib import admin
from .models import Category, Product, Ingredient, CategoryIngredient
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','ingredient','quantity',  'category', 'price', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'category__name')
    list_filter = ('is_active', 'category')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('category_ingredient','quantity', 'price',  'is_active', 'created_at', 'updated_at')
    list_filter = ('category_ingredient', 'is_active',)  


@admin.register(CategoryIngredient)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active',)