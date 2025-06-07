from rest_framework import serializers
from .models import Usuario, Avaliacao

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'saldo', 'vendas_realizadas', 'compras_realizadas', 'avaliacao_media']
        
class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'
