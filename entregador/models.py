from django.db import models
from usuarios.models import Usuario
from animais.models import Animal

class Entregador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, limit_choices_to={'tipo': 'entregador'}, related_name='entregador', null=True)
    nome = models.CharField(max_length=100)
    placa = models.CharField(max_length=10)
    tipo_preco = models.CharField(max_length=20, choices=[
        ('por_km', 'Por Km'),
        ('por_kg', 'Por Kg'),
        ('fixo', 'Fixo')
    ])
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    cpf = models.CharField(max_length=14, unique=True)
    pix = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.usuario.username} ({self.tipo_preco} - R$ {self.valor})"


class Entrega(models.Model):
    entregador = models.ForeignKey(Entregador, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('aceita', 'Aceita'),
        ('confirmada', 'Confirmada'),
    ], default='pendente')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entrega de {self.animal.nome} por {self.entregador.usuario.username}"

