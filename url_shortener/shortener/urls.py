from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_url, name='create_url'),
    path('edit/<int:id>/', views.edit_url, name='edit_url'),
    path('delete/<int:id>/', views.delete_url, name='delete_url'),
    path('<str:short_key>/', views.redirect_url, name='redirect'),
]
