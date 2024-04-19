import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from autoslug.fields import AutoSlugField
from tinymce.models import HTMLField

from accounts.models import CustomUser

class Project(models.Model):
    difficulty_choices = {
        '0': 'beginner',
        '1': 'intermediate',
        '2': 'advanced'
    }
    
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(verbose_name='Project Name', max_length=200, unique=True)
    short_description = models.CharField(verbose_name='Project Description', max_length=1000)
    long_description = HTMLField()
    tags = ArrayField(
        models.CharField(verbose_name='Project Tags', max_length=200, default=''),
        default=list
    )
    enrolled_profiles = models.ManyToManyField(CustomUser, related_name='enrolled_projects', blank=True)
    difficulty = models.CharField(verbose_name='Project Difficulty', max_length=1, choices=difficulty_choices)
    project_slug = AutoSlugField(populate_from='name', unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created', '-date_updated')
        
    def __str__(self):
        return f'{self.name} by {self.creator.username}'

class Solution(models.Model):
    name = models.CharField(verbose_name='Solution Name', max_length=500, default='')
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='solutions')
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='project')
    repo_link = models.URLField(verbose_name='Solution Repository', max_length=500)
    live_link = models.URLField(verbose_name='live Solution', max_length=500, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created', '-date_updated')

    def __str__(self):
        return f'Solution by {self.creator.username}'