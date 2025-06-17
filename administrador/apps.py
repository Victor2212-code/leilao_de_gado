from django.apps import AppConfig



class AdministradorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'administrador'  # Verifique se este nome corresponde ao nome do diretório do app
        
    def ready(self):
        import administrador.signals

