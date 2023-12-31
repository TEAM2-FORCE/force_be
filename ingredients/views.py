from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .models import *
from .serializers import *
from products.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated



class IgdList(APIView):

    # 전체 성분 조회
    def get(self, request, format = None):
        igds = Ingredient.objects.all().order_by('igd_name')
        serializer = IgdSerializer(igds, many = True, context={'request':request}) #다수 객체 이용
        return Response(serializer.data)

    # 성분 데이터 DB 저장
    def post(self, request, format = None):
        data = request.data
        serializer = IgdSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class IgdDetail(APIView):

    # 개별 성분 조회
    def get(self, request, id):
        igd = get_object_or_404(Ingredient, igd_id = id)
        serializer = IgdSerializer(igd, context={'request':request})
        return Response(serializer.data)


class IgdBm(APIView):

    permission_classes = [IsAuthenticated]

    # 북마크한 성분 전체 조회
    def get(self, request, format = None):
        bm_lists = Bookmark.objects.filter(user = request.user)
        serializer = IgdBmSerializer(bm_lists, many = True, context={'request':request}) #다수 객체 이용
        return Response(serializer.data)

    # 성분 북마크하기
    def post(self, request, igd_id, foramt = None):

        try :
            igd = Ingredient.objects.get(igd_id = igd_id)
        except Ingredient.DoesNotExist:
            return Response({"error" : "Ingredients not found"}, status = status.HTTP_404_NOT_FOUND)


        data = {
            "user" : request.user.id,
            "igd" : igd.igd_id,
        }

        serializer = IgdBmSerializer(data = data, context={'request':request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    # 성분 북마크 삭제하기
    def delete(self, request, igd_id):
        igd = get_object_or_404(Bookmark, igd_id = igd_id)
        igd.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action

# 성분 검색
class IgdSearchListView(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IgdSerializer
    search_fields = ('igd_name',)
    filter_backends = [SearchFilter]

from .filters import IgdCautionFilter

# 주의성분 필터링
class IgdFilterListView(generics.ListAPIView) :
    serializer_class = IgdSerializer
    filter_class = IgdCautionFilter

    def get_queryset(self):
        queryset = Ingredient.objects.all()

        igd_caution_param = self.request.query_params.get('igd_caution')

        if igd_caution_param is not None:
            igd_caution = igd_caution_param.lower() == 'true'
            queryset = queryset.filter(igd_caution=igd_caution)

        return queryset


class IngredientProducts(APIView):
    def get_object(self, id):
        try:
            return Ingredient.objects.get(igd_id=id)
        except Ingredient.DoesNotExist:
            raise Http404

    def get(self, request, id):
        ingredient = self.get_object(id)
        products = ingredient.products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        ingredient = self.get_object(id)
        product_data = request.data.copy()
        product_data['ingredients'] = [ingredient.igd_id]  # 제품과 연결하기 위해 product pk 추가

        product_serializer = ProductSerializer(data=product_data)

        if product_serializer.is_valid():
            # 성분 생성
            ingredient = product_serializer.save()

            return Response(product_serializer.data, status=status.HTTP_201_CREATED)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


