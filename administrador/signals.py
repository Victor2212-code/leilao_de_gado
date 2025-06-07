# administrador/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import LogAuditoria
from django.utils.timezone import now

@receiver(user_logged_in)
def registrar_login(sender, request, user, **kwargs):
    LogAuditoria.objects.create(usuario=user, acao="Login realizado", data_hora=now())
