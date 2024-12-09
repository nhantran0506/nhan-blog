from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser): # already contain fields that needed
    user_id = models.UUIDField(primary_key = True, db_index = True, auto_created = True)
    birth_date = models.DateField(null=True, blank=True)
    
    
    
    