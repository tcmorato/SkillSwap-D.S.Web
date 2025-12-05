from site_tulio import views
from django.urls import path


urlpatterns = [
    path('', views.listarPost.as_view(), name = 'inicio'),
    path('postar/', views.criarPost.as_view(), name = 'postar'),
    path('signup/', views.signup, name = 'signup'),
    path('deletar/<int:pk>/', views.deletarPost.as_view(), name = 'deletar'),
    path('editar/<int:pk>/', views.editarPost.as_view(), name = 'editar')
]