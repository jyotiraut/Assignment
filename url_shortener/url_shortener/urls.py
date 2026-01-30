from django.contrib import admin
from django.urls import path, include
from shortener.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('', include('shortener.urls')),
    path('', include('django.contrib.auth.urls')),
]
