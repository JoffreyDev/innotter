from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    image = models.ImageField(null=True, blank=True, upload_to='users_images')
    role = models.CharField(max_length=9, choices=Roles.choices, default='user')
    title = models.CharField(max_length=80, blank=True)
    is_blocked = models.BooleanField(default=False)
    
