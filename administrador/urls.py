from django.urls import path
from .views import gerenciar_usuarios, banir_usuario, desbanir_usuario, relatorios_estatisticas, auditoria_sistema

app_name = "administrador"  # Define um namespace para as URLs

urlpatterns = [
    path('gerenciar_usuarios/', gerenciar_usuarios, name='gerenciar_usuarios'),
    path('auditoria/', auditoria_sistema, name='auditoria'),
    path('estatisticas/', relatorios_estatisticas, name='estatisticas'),
    path('banir_usuario//<int:user_id>/', banir_usuario, name='banir_usuario'),
    path('desbanir_usuario//<int:user_id>/', desbanir_usuario, name='desbanir_usuario'),
]
