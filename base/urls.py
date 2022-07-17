from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar-grupo/', views.cadastrarGrupo, name='cadastrar-grupo'),
    path('cadastrar-equipe/', views.cadastrarEquipe, name='cadastrar-equipe'),
    path('cadastrar-líder/', views.cadastrarLíder, name='cadastrar-líder'),
    path('cadastrar-cabo/', views.cadastrarCabo, name='cadastrar-cabo'),
    #     path('cadastrar-eleitor/', views.cadastrarEleitor, name='cadastrar-eleitor'),
]
