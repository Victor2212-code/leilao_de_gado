# entregador/urls.py
from django.urls import path
from . import views

app_name = 'entregador'  # ESSENCIAL para o uso de {% url 'entregador:...' %}

urlpatterns = [
    path('visualizar/', views.visualizar_entregas, name='visualizar_entregas'),
    path('aceitar/', views.aceitar_entrega, name='aceitar_entrega'),
    path('confirmar/', views.confirmar_entrega, name='confirmar_entrega'),
    path('atualizar/', views.atualizar_dados, name='atualizar_dados'),
    path('cadastro_entregador/', views.cadastro_entregador, name='cadastro_entregador'),
    path('salvar_entregador/', views.salvar_entregador, name='salvar_entregador'),
]
