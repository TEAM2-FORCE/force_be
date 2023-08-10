from django.db import models

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
    pd_name = models.TextField(verbose_name="제품 이름") 
    pd_price = models.IntegerField(verbose_name="제품 가격")
    pd_brand = models.CharField(max_length=20, verbose_name="제품 브랜드명")
    pd_purpose = models.CharField(max_length=500, verbose_name="제품 사용 목적")
    pd_usage = models.CharField(max_length=500, verbose_name="제품 사용법")
    pd_like_cnt = models.IntegerField(verbose_name="찜 개수")
    pd_image = models.ImageField(null=True, blank=True, verbose_name="제품 대표 사진")
    cg_id = models.IntegerField(choices=CHOICES)

class Market(BaseModel):
    mk_id = models.AutoField(primary_key=True)
    mk_name = models.CharField(max_length=20, verbose_name="구매처 이름")
    pd_id = models.ForeignKey(to=Product, on_delete=models.CASCADE)