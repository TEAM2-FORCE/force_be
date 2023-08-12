from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Product, Market, Vegan, Wishlist, ProductIngredient
from .serializers import ProductSerializer, MarketSerializer, VeganSerializer, WishlistSerializer

from ingredients.serializers import IgdSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from rest_framework.generics import ListAPIView
from rest_framework.exceptions import NotFound

from rest_framework.permissions import IsAuthenticated

from rest_framework import generics
from rest_framework.filters import SearchFilter

class ProductsList(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        sort_std = self.request.query_params.get('sort', 'default')
        product_query = Product.objects.all()

        if sort_std == 'default':
            products = product_query.order_by('-pd_like_cnt')
        
        elif sort_std == 'name':
            products = product_query.order_by('pd_name')
        
        elif sort_std == 'price':
            products = product_query.order_by('pd_price')

        elif sort_std == '-price':
            products = product_query.order_by('-pd_price')
        else:
            products = product_query
        
        return products
    
    def post(self, request, format=None):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
    
class ProductDetail(APIView):
    def get_object(self, id):
        try:
            return Product.objects.get(pd_id=id)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")

    def get(self, request, id):
        product = self.get_object(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = Product.objects.get(pd_id=id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = Product.objects.get(pd_id=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductCategory(APIView):
    def get(self, request, cg_id):
        sort_std = self.request.query_params.get('sort', 'default')
        product_query = Product.objects.filter(cg_id=cg_id)

        if sort_std == 'default':
            products = product_query.order_by('-pd_like_cnt')
        
        elif sort_std == 'name':
            products = product_query.order_by('pd_name')
        
        elif sort_std == 'price':
            products = product_query.order_by('pd_price')

        elif sort_std == '-price':
            products = product_query.order_by('-pd_price')
        else:
            products = product_query
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductSearchListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ('pd_name', 'pd_brand')
    filter_backends = [SearchFilter]
    
class MarketList(APIView):
    def post(self, request, id): 
        request_data_copy = request.data.copy() # mutable 한 딕셔너리로 카피하는 메서드
        request_data_copy['product'] = id
        serializer = MarketSerializer(data=request_data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        markets = Market.objects.filter(product=id)
        serializer = MarketSerializer(markets, many=True)
        return Response(serializer.data)
    
class VeganList(APIView):
    def post(self, request, id): 
        request_data_copy = request.data.copy() 
        request_data_copy['product'] = id
        serializer = VeganSerializer(data=request_data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        vegans = Vegan.objects.filter(product=id)
        serializer = VeganSerializer(vegans, many=True)
        return Response(serializer.data)

class WishlistList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        wishlist = Wishlist.objects.filter(user = request.user)
        serializer = WishlistSerializer(wishlist, many = True)
        return Response(serializer.data)

    def post(self, request, id, foramt = None):
        try :
            product = Product.objects.get(pd_id = id)
        except Product.DoesNotExist:
            return Response({"error" : "Products not found"}, status = status.HTTP_404_NOT_FOUND)

        data = {
            "user" : request.user.id, 
            "product" : product.pd_id,
        }

        serializer = WishlistSerializer(data = data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else : 
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pd_id = id)
        product.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class ProductIngredients(APIView):
    def get_object(self, id):
        try:
            return Product.objects.get(pd_id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id):
        product = self.get_object(id)
        ingredients = product.ingredients.all()  # 다대다 관계에서 ingredients 가져오기
        serializer = IgdSerializer(ingredients, many=True)
        return Response(serializer.data)
    
    def post(self, request, id):
        product = self.get_object(id)
        ingredient_data = request.data.copy()
        ingredient_data['products'] = [product.pd_id]

        ingredient_serializer = IgdSerializer(data=ingredient_data)
        
        if ingredient_serializer.is_valid():
            # 성분 생성
            ingredient = ingredient_serializer.save()

            # 성분과 제품 연결
            product.ingredients.add(ingredient)

            return Response(ingredient_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(ingredient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


