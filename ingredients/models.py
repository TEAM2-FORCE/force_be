from django.db import models

class BaseModel(models.Model) :
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add = True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now = True)
    
    class Meta:
        abstract = True

class Ingredients(BaseModel) :
    igd_id = models.AutoField(verbose_name = "성분id", primary_key = True)
    igd_name = models.CharField(verbose_name = "성분명", max_length = 20, null = False)
    igd_main_ftn = models.TextField(verbose_name = "성분메인기능", null = False)
    igd_plants = models.BooleanField(verbose_name = "식물성", null = True)
