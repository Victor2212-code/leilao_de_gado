from django.db import models
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class LogAuditoria(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    acao = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.acao} em {self.data_hora}"
