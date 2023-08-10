from django.db import models
<<<<<<< HEAD
from django.conf import settings
=======
from ingredients.models import Ingredient
>>>>>>> develop

class BaseModel(models.Model):
    class Meta:
        abstract = True

class Product(BaseModel):
    CHOICES = (
        ('1', 'makeup'),
        ('2', 'skincare'),
        ('3', 'mask'),
        ('4', 'suncare')
    )

    pd_id = models.AutoField(primary_key=True)
    pd_name = models.TextField(verbose_name="상품 이름") 
    pd_price = models.IntegerField(verbose_name="상품 가격")
    pd_brand = models.CharField(max_length=20, verbose_name="상품 브랜드명")
    pd_purpose = models.CharField(max_length=500, verbose_name="상품 사용 목적")
    pd_usage = models.CharField(max_length=500, verbose_name="상품 사용법")
    pd_like_cnt = models.IntegerField(verbose_name="찜 개수")
    pd_image = models.ImageField(null=True, blank=True, verbose_name="상품 대표 사진")
    cg_id = models.IntegerField(choices=CHOICES)
    ingredients = models.ManyToManyField(Ingredient, verbose_name="상품이 포함하는 성분들", blank=True)

class Market(BaseModel):
    mk_id = models.AutoField(primary_key=True)
    mk_name = models.CharField(max_length=20, verbose_name="구매처 이름")
    mk_link = models.URLField(max_length=500)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, blank=False)

class Vegan(BaseModel):
    VEGAN_CHOICES = (
        ('Korea agency of Vegan Certification and Services', '한국비건인증원'),
        ('Expertise Vegan Europe', '프랑스이브비건'),
        ('V Label Italia srl', '이탈리아브이라벨'),
        ('The Vegan Society', '영국비건소사이어티'),
        ('PETA Beauty without bunny - global animal test-free', 'PETA1'),
        ('PETA Beauty without bunny - global animal test-free and vegan', 'PETA2'),
        ('Biorius', '벨기에 바이오리우스')
    )
    vg_id = models.AutoField(primary_key=True)
    vg_company = models.CharField(choices=VEGAN_CHOICES, max_length=70, verbose_name="비건 인증처명")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, blank=False)

class Wishlist(BaseModel) :
    wish_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "wish_product_id", on_delete = models.CASCADE)
    product = models.OneToOneField(Product, on_delete = models.CASCADE)