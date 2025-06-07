from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta

User = get_user_model()

# Função para definir a data padrão de término do leilão
def default_termino_leilao():
    return now() + timedelta(days=7)  # Define um prazo padrão de 7 dias

class Animal(models.Model):
    vendedor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="animais_vendidos"
    )
    nome = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=7, decimal_places=2)  
    idade = models.IntegerField()
    raca = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='animais/', null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=[('Disponível', 'Disponível'), ('Vendido', 'Vendido')], 
        default='Disponível'
    )
    valor_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    termino_leilao = models.DateTimeField(default=default_termino_leilao)  # Chama a função corretamente
    
    def __str__(self):
        return f"{self.nome} - {self.raca} ({self.status})"
