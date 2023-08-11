from django.contrib import admin
from .models import *
from products.models import ProductIngredient
# Register your models here.

#admin.site.register(Ingredient)
admin.site.register(Bookmark)

class IngredientProdcutInline(admin.TabularInline):  
    model = ProductIngredient

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = [
        IngredientProdcutInline,  
    ]