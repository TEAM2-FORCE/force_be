from django.db import models
from django.conf import settings


class BaseModel(models.Model) :
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add = True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now = True)
    
    class Meta:
        abstract = True

class Ingredient(BaseModel) :
    igd_id = models.AutoField(verbose_name = "성분id", primary_key = True) #pk 명시
    igd_name = models.CharField(verbose_name = "성분명", max_length = 20, null = False)
    igd_main_ftn = models.TextField(verbose_name = "성분메인기능", null = False)
    igd_plants = models.BooleanField(verbose_name = "식물성", null = True)
    
    # 상품에서 성분 역참조 이름 ingredient_products 명시
    # circular import 피하기 위해서 'proudcts.Product'로 지연 import
    # 성분 등록 시, product 지정 안해줘도 되게끔 null, default 지정 (데이터 등록 선후관계 상 성분이 먼저 입력되어야 한다고 판단)
    products = models.ForeignKey('products.Product',  on_delete = models.CASCADE, related_name='ingredient_products', verbose_name="성분을 포함하는 상품들", blank=True, null=True, default = None)

class Bookmark(BaseModel) :
    bm_id = models.AutoField(verbose_name = "북마크id", primary_key = True) #pk 명시
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "bm_igd_id", on_delete = models.CASCADE) #user_id는 여러개의 북마크를 지정 가능 (1:N 관계), 역참조 시 bm_igd_id
    igd = models.OneToOneField(Ingredient, on_delete = models.CASCADE) #igd_id는 하나의 북마크를 가짐 (1:1 관계)

 # 다대다 관계를 일대다, 다대일로 풀기 위한 중간 모델 생성
class IngredientProduct(BaseModel):
    ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete = models.CASCADE)   
