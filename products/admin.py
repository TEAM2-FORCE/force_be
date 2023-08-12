from django.contrib import admin
from .models import *
from ingredients.models import IngredientProduct
# Register your models here.

#admin.site.register(Product)
admin.site.register(Wishlist)

class ProductIngredientInline(admin.TabularInline):  
    model = IngredientProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductIngredientInline,  
    ]