from django.contrib import admin
from .models import *
from ingredients.models import IngredientProduct
# Register your models here.

#admin.site.register(Product)
admin.site.register(Wishlist)

class ProductIngredientInline(admin.TabularInline):  
    model = IngredientProduct

class ProductVeganInline(admin.TabularInline):
    model = Vegan

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductIngredientInline, 
    ]

@admin.register(Vegan)
class ProductVeganAdmin(admin.ModelAdmin):
    pass