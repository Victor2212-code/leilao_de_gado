# Exemplo de uso de request em ModelAdmin
from django.contrib import admin
from .models import LogAuditoria

class LogAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()

admin.site.register(LogAuditoria, LogAdmin)
