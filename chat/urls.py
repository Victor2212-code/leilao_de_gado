from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('', views.chat, name='chat'),
    path('<int:usuario_id>/', views.chat, name='chat_usuario'),
    path('buscar/', views.buscar_usuarios, name='buscar_usuarios'),
    path('enviar_mensagem/<int:usuario_id>/', views.enviar_mensagem, name='enviar_mensagem'),
]

