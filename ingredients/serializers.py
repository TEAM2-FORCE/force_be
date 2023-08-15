from rest_framework import serializers
from .models import *

class IgdSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Ingredient
        fields = "__all__"

     # 북마크 여부를 나타내는 커스텀 필드 추가
    bookmarked_igd = serializers.SerializerMethodField()

    def get_bookmarked_igd(self, obj):
        # 북마크한 성분(Ingredient)이 있는지 확인하여 True 또는 False 반환
        user = self.context.get('request').user
        
        if user.is_authenticated:
            # 해당 유저가 북마크한 성분(Ingredient) 목록 가져오기
            bookmarked_ingredients = user.bm_igd_id.all()

            # 현재 북마크 객체의 igd가 bookmarked_ingredients에 포함되어 있는지 확인
            return bookmarked_ingredients.filter(igd=obj).exists()
        
        return False

class IgdBmSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Bookmark
        fields = "__all__"
    # IngredientSerializer를 중첩하여 북마크한 Ingredient의 내용을 직렬화
    ingredient_contents = IgdSerializer(source='igd', read_only=True)
  