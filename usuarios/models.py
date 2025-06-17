from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    TIPOS_USUARIO = [
        ('comprador', 'Comprador'),
        ('vendedor', 'Vendedor'),
        ('administrador', 'Administrador'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='comprador')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vendas_realizadas = models.IntegerField(default=0)
    compras_realizadas = models.IntegerField(default=0)
    avaliacao_media = models.FloatField(default=0.0)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios_usuario_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarios_usuario_permissions',
        blank=True,
    )

    def is_vendedor(self):
        return self.tipo == 'vendedor'

    def is_comprador(self):
        return self.tipo == 'comprador'

    def is_administrador(self):
        return self.tipo == 'administrador'

    def __str__(self):
        return f"{self.username} ({self.get_tipo_display()})"


class Avaliacao(models.Model):
    avaliador = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='avaliador')
    avaliado = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='avaliado')
    nota = models.IntegerField()
    comentario = models.TextField()

    def __str__(self):
        return f"Avaliação de {self.avaliador.username} para {self.avaliado.username} - Nota: {self.nota}"


class Lance(models.Model):
    comprador = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, limit_choices_to={'tipo': 'comprador'})  
    animal = models.ForeignKey('animais.Animal', on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('Aguardando', 'Aguardando'),
        ('Aprovado', 'Aprovado'),
        ('Rejeitado', 'Rejeitado')
    ], default='Aguardando')
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lance de {self.comprador.username} no animal {self.animal.nome}: R$ {self.valor}"


class Animal(models.Model):
    nome = models.CharField(max_length=100)
    raca = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    idade = models.IntegerField()
    status = models.CharField(max_length=20, choices=[
        ('Disponível', 'Disponível'),
        ('Vendido', 'Vendido'),
        ('Removido', 'Removido')
    ], default='Disponível')
    imagem = models.ImageField(upload_to='animais/', null=True, blank=True)
    valor_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    vendedor = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, limit_choices_to={'tipo': 'vendedor'})  # Somente vendedores podem cadastrar animais

    def __str__(self):
        
        return f"{self.nome} - {self.raca}"


class Endereco(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='endereco')
    cep = models.CharField(max_length=9, help_text="Formato: 00000-000")
    estado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10, help_text="Número da residência")
    complemento = models.CharField(max_length=255, blank=True, null=True, help_text="Opcional")
    telefone = models.CharField(max_length=15, help_text="Formato: (99) 99999-9999")
    cpf = models.CharField(max_length=14, unique=True, help_text="Formato: 000.000.000-00")
    
    def __str__(self):
        return f"{self.usuario.username} - {self.rua}, {self.numero}, {self.bairro}, {self.cidade} - {self.estado}"