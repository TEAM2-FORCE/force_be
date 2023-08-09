from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

class ProductsList(APIView):
    def get(self, request, format=None):
        sort_by = request.query_params.get('sort', 'default')

        if sort_by == 'price':
            products = Product.objects.all().order_by('pd_price')
        elif sort_by == 'lowprice':
            products = Product.objects.all().order_by('-pd_price')
        else:
            products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

class ProductsList(ListAPIView):
    def get(self, request, format=None):
        sort_standard = self.request.query_params.get('sort', 'default')

        if sort_standard == 'default':
            products = Product.objects.all().order_by('-pd_like_cnt')
        
        elif sort_standard == 'name':
            products = Product.objects.all().order_by('pd_name')
        
        elif sort_standard == 'price':
            products = Product.objects.all().order_by('pd_price')

        elif sort_standard == 'lowprice':
            products = Product.objects.all().order_by('-pd_price')
        else:
            products = Product.objects.all()
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
        
        # products = Product.objects.all()
        # serializer = ProductSerializer(products, many=True) # 많은 값을 가져올 때는 다중값인 'many'를 True로 한다. 
        # return Response(serializer.data)
# class PostModelViewSet(viewsests.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     filter_backends = [SearchFilter, OrderingFilter]

#     search_fidels = ['message'] # ?serch= -> QuerySet조건 절에 추가할 필드 지정, 문자열 필드만 지정 가능

#     ordering_fields = ['id'] # ?ordering= -> 정렬을 허용할 필드 지정, 미지정 시에 serializer_class에 지정된 필드 사용
#     ordering = ['id'] # 디폴트 정렬 지정
    
class ProductDetail(APIView):
    def get_object(self, id):
        product = Product.objects.get(id=Product.pd_id)
        self.check_object_permissions(self.request, product)
        return product
    
    def get(self, request, id):
        product = Product.objects.get(pd_id=id)
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
        products = Product.objects.filter(cg_id=cg_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)