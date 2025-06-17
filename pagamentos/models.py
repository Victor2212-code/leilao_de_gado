from django.db import models
from usuarios.models import Lance

class Transacao(models.Model):
    lance = models.ForeignKey(Lance, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('Pendente', 'Pendente'),
        ('Pago', 'Pago')
    ], default='Pendente')

    def __str__(self):
        return f"Transação {self.id} - {self.status}"
