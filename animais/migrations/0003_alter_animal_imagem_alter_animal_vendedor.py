from django.db import migrations, models
import django.contrib.auth.models
from django.conf import settings

def set_default_vendedor(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)  # Obtém o modelo de usuário
    default_user = User.objects.first()  # Pega o primeiro usuário como padrão
    if not default_user:
        default_user = User.objects.create(username="admin", email="admin@example.com")  # Cria um admin padrão
    Animal = apps.get_model('animais', 'Animal')  
    for animal in Animal.objects.all():
        animal.vendedor = default_user
        animal.save()

class Migration(migrations.Migration):

    dependencies = [
        ('animais', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),  # Ajuste de acordo com sua versão
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='vendedor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL),
        ),
        migrations.RunPython(set_default_vendedor),  # Aplica um vendedor padrão
        migrations.AlterField(
            model_name='animal',
            name='vendedor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
    ]
