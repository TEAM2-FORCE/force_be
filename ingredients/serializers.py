from rest_framework import serializers
from .models import *

class IgdSerializer(serializers.ModelSerializer):
    # products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Ingredient
        fields = "__all__"

class IgdBmSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bookmark
        fields = "__all__"