from django.db import models
from django.urls import reverse
from django.conf import settings

# User < AbstractUser < AbstractBaseUser 
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings', blank=True)

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("accounts:user_page", kwargs={"user_id": self.pk})
    
    