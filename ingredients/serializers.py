from rest_framework import serializers
from .models import *
#from products.serializers import ProductSerializer

class IgdSerializer(serializers.ModelSerializer):
    #products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Ingredient
        fields = "__all__"

    def get_product_serializer():
        from products.serializers import ProductSerializer
        return ProductSerializer(many=True, read_only=True)

class IgdBmSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bookmark
        fields = "__all__"