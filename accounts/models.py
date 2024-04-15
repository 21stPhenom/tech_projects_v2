from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    ranking = models.PositiveIntegerField(verbose_name='User rank', default=0)
    projects_completed = models.PositiveIntegerField(verbose_name='Projects Completed', default=0)
    
    class Meta:
        ordering = ('-date_joined',)

    def __str__(self):
        return f'{self.username}'