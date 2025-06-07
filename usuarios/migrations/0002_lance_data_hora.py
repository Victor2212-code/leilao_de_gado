import django.utils.timezone
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lance',
            name='data_hora',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
