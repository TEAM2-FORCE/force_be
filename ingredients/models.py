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

class Bookmark(BaseModel) :
    bm_id = models.AutoField(verbose_name = "북마크id", primary_key = True) #pk 명시
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "bm_igd_id", on_delete = models.CASCADE) #user_id는 여러개의 북마크를 지정 가능 (1:N 관계), 역참조 시 bm_igd_id
    igd = models.OneToOneField(Ingredient, on_delete = models.CASCADE) #igd_id는 하나의 북마크를 가짐 (1:1 관계)
