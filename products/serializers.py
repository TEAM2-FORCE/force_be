from rest_framework import serializers
from .models import Products

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__" # db(즉 모델)의 모든 필드 가져오기
