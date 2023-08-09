from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser) :
    email = models.CharField(max_length = 50, unique = True, blank = True, null = True)

    