from rest_framework import serializers
from .models import Product, Market, Vegan, Wishlist

import boto3
from config.settings import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
VALID_IMAGE_EXTENSIONS = [ "jpg", "jpeg", "png", "gif" ]

class ProductSerializer(serializers.ModelSerializer):
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
                return data
            except:
                raise serializers.ValidationError("Invalid Image File")

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
          model = Market
          fields = "__all__"

class VeganSerializer(serializers.ModelSerializer):
    class Meta:
          model = Vegan
          fields = "__all__"

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"