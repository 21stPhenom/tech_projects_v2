from django.contrib import admin

from projects.models import Project, Solution

admin.site.register((Project, Solution))