from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
import uuid

class UserRole(Enum):
    USER = 'User'
    ADMIN = 'Admin'

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, db_index=True, auto_created=True, default=uuid.uuid4, editable=False)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[(role.name, role.value) for role in UserRole],
        default=UserRole.USER.name,
    )
    refresh_token = models.CharField(max_length=100000, null=True, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.URLField(null=True, blank=True)
    
    
    