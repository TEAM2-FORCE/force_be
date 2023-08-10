from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser) :
    id = models.AutoField(verbose_name = "유저id", primary_key=True)
    email = models.CharField(max_length = 50, unique = True, blank = True, null = True)

    
