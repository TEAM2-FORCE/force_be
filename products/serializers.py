from rest_framework import serializers
from .models import Product, Market, Vegan, Wishlist

from ingredients.serializers import IgdSerializer

import boto3
from config.settings import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
VALID_IMAGE_EXTENSIONS = [ "jpg", "jpeg", "png", "gif" ]

class IngredientFilterSerializer(serializers.Serializer):
    include_ingredients = serializers.ListField(required=False, allow_empty=True, child=serializers.CharField(max_length=255))
    exclude_ingredients = serializers.ListField(required=False, allow_empty=True, child=serializers.CharField(max_length=255))
    certification_names = serializers.ListField(required=False, allow_empty=True, child=serializers.CharField(max_length=255))

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
          model = Market
          fields = "__all__"

class VeganSerializer(serializers.ModelSerializer):
    class Meta:
          model = Vegan
          fields = "__all__"



class ProductSerializer(serializers.ModelSerializer):
    ingredients = IgdSerializer(many=True, read_only=True)
    vegan_cert = VeganSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def validate(self, data): 
            image = data.get('pd_image')

            if not image.name.split('.')[-1].lower() in VALID_IMAGE_EXTENSIONS:
                serializers.ValidationError("Not an Image File")
            s3 = boto3.client('s3',
                aws_access_key_id = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
                region_name = AWS_REGION)
            try:
                s3.upload_fileobj(image, AWS_STORAGE_BUCKET_NAME, image.name)
                img_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{image.name}"
                data['pd_image'] = img_url
                print(img_url)
                return data
            except:
                raise serializers.ValidationError("Invalid Image File")
    
    wished_pd = serializers.SerializerMethodField()

    def get_wished_pd(self, obj):
        user = self.context.get('request').user
        
        if user.is_authenticated:
            wished_products = user.wish_product_id.all()
            return wished_products.filter(product=obj).exists()
        
        return False
    
class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"
    
    products_contents = ProductSerializer(source='product', read_only=True)

class ProductGetSerializer(serializers.ModelSerializer):
    # pd_image = Product.CharField(null=True, blank=True, verbose_name="상품 대표 사진")
    pd_image = serializers.CharField(source="product.pd_image", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

