from site_tulio import views
from django.urls import path

urlpatterns = [
    path('', views.inicio, name = 'inicio'),
    path('postar/', views.postar, name = 'postar'),
]
