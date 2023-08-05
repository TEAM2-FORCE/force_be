from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser) :
    # name = models.CharField(max_length = 10, blank = True, null = True)
    # username = models.CharField(max_length = 10, unique = True, blank = True, null = True)
    # social_id = models.CharField(max_length = 50, blank = True, null = True)
    email = models.CharField(max_length = 254, unique = True, blank = True, null = True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = [
    #     'name',
    #     'username'
    #     'social_id'
    # ]

    # def __str__(self):
    #     return self.email