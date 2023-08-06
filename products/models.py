from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True) # 챌린지 과제: filter orm을 이용하기. 더미데이터를 만들어서 get으로 불러오는데 시간을 조건으로 해서 불러오기. 
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta:
        abstract = True

class Products(BaseModel):
    CHOICES = (
        ('1', '스킨케어'),
        ('2', '선케어'),
        ('3', '샴푸')
    )

    product_id = models.AutoField(primary_key=True)
    procuct_name = models.CharField(max_length=50, verbose_name="제품 이름") 
    product_price = models.IntegerField(verbose_name="제품 가격")
    product_brand = models.CharField(max_length=20, verbose_name="제품 브랜드명")
    product_purpose = models.CharField(max_length=500, verbose_name="제품 사용 목적")
    pd_usage = models.CharField(max_length=500, verbose_name="제품 사용법")
    pd_like_cnt = models.IntegerField(verbose_name="찜 개수")
    # product_image = models.ImageField(verbose_name="제품 대표 사진") # S3 연결 후 시도해보기

    cg_id = models.IntegerField(choices=CHOICES) # INtegerChoices?
    cg_name = models.CharField(choices=CHOICES, max_length=20)


# ? category를 굳이 테이블로 만들 필요가 없을듯? category를 추가, 수정, 삭제하는건 아니니까!
# class Category(BaseModel):
#     CHOICES = (
#         ('1', '스킨케어'),
#         ('2', '선케어'),
#         ('3', '샴푸')
#     )
#     cg_id = models.AutoField(primary_key=True)
#     cg_name = models.CharField(choices=CHOICES, max_length=20)


