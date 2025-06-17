from django.urls import path
from .views import  animal_detalhes, aceitar_lance, rejeitar_lance, buscar_animais

urlpatterns = [
    path('animal/<int:animal_id>/', animal_detalhes, name='animal_detalhes'),
    path('aceitar_lance/<int:lance_id>/', aceitar_lance, name='aceitar_lance'),
    path('rejeitar_lance/<int:lance_id>/', rejeitar_lance, name='rejeitar_lance'),
    path('buscar/', buscar_animais, name='buscar_animais'),
]
