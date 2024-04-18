from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('/', include('projects.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'))
]