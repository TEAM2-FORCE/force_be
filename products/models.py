from django.db import models

from django.conf import settings

from ingredients.models import Ingredient

class BaseModel(models.Model):
    class Meta:
        abstract = True

class Vegan(BaseModel):
    VEGAN_CHOICES = (
        ('Korea agency of Vegan Certification and Services', '한국비건인증원'),
        ('Expertise Vegan Europe', '프랑스이브비건'),
        ('V Label Italia srl', '이탈리아브이라벨'),
        ('The Vegan Society', '영국비건소사이어티'),
        ('PETA Beauty without bunny - global animal test-free', 'PETA1'),
        ('PETA Beauty without bunny - global animal test-free and vegan', 'PETA2'),
    )
    vg_id = models.AutoField(primary_key=True)
    vg_company = models.CharField(choices=VEGAN_CHOICES, max_length=70, verbose_name="비건 인증처명")

class Product(BaseModel):
    CHOICES = (
        (1, 'makeup'),
        (2, 'skincare'),
        (3, 'mask'),
        (4, 'suncare')
    )

    pd_id = models.AutoField(primary_key=True)
    pd_name = models.TextField(verbose_name="상품 이름") 
    pd_price = models.IntegerField(verbose_name="상품 가격")
    pd_brand = models.CharField(max_length=20, verbose_name="상품 브랜드명")
    pd_purpose = models.CharField(max_length=500, verbose_name="상품 사용 목적")
    pd_usage = models.CharField(max_length=500, verbose_name="상품 사용법")
    pd_like_cnt = models.IntegerField(verbose_name="찜 개수")
    pd_image = models.ImageField(null=True, blank=True, verbose_name="상품 대표 사진")
    cg_id = models.IntegerField(choices=CHOICES, null = True) #에러 막기 위한 null 값 
    vegan_cert = models.ManyToManyField(Vegan,blank=True, verbose_name="비건 인증처")

    # 성분에서 상품 역참조 이름 product_ingredients로 명시
    ingredients = models.ManyToManyField(Ingredient, through='ProductIngredient', related_name='products_ingredient', blank=True)

class Wishlist(BaseModel) :
    wish_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "wish_product_id", on_delete = models.CASCADE)
    product = models.OneToOneField(Product, on_delete = models.CASCADE)

class Market(BaseModel):
    mk_id = models.AutoField(primary_key=True)
    mk_name = models.CharField(max_length=20, verbose_name="구매처 이름")
    mk_link = models.URLField(max_length=500)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, blank=False)

# 다대다 관계를 일대다, 다대일로 풀기 위한 중간 모델 생성
class ProductIngredient(BaseModel):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'product_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE, related_name = 'ingredient_products')   