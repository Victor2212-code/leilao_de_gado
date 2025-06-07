from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Mensagem(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    conteudo = models.TextField()
    lida = models.BooleanField(default=False)
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.remetente.username} para {self.destinatario.username} - {self.data_envio.strftime('%d/%m/%Y %H:%M')}"
