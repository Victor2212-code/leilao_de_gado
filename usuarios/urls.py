from django.urls import path
from .views import index, login_view, cadastro_view, dashboard, cadastrar_animal, \
logout_view, atualizar_ranking, buscar_vencedor, salvar_endereco

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('cadastro/', cadastro_view, name='cadastro'),
    path('dashboard/', dashboard, name='dashboard'),
    path('cadastrar_animal/', cadastrar_animal, name='cadastrar_animal'),
    path('logout/', logout_view, name='logout'),
    path('atualizar_ranking/<int:animal_id>/', atualizar_ranking, name='atualizar_ranking'),
    path('buscar_vencedor/<int:animal_id>/', buscar_vencedor, name='buscar_vencedor'),
    path('cadastro/', cadastro_view, name='cadastro'),
    path('salvar-endereco/', salvar_endereco, name='salvar_endereco'),
]
