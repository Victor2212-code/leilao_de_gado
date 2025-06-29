# Generated by Django 5.1.6 on 2025-02-24 17:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_alter_usuario_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(help_text='Formato: 00000-000', max_length=9)),
                ('estado', models.CharField(max_length=50)),
                ('cidade', models.CharField(max_length=100)),
                ('bairro', models.CharField(max_length=100)),
                ('rua', models.CharField(max_length=255)),
                ('numero', models.CharField(help_text='Número da residência', max_length=10)),
                ('complemento', models.CharField(blank=True, help_text='Opcional', max_length=255, null=True)),
                ('telefone', models.CharField(help_text='Formato: (99) 99999-9999', max_length=15)),
                ('cpf', models.CharField(help_text='Formato: 000.000.000-00', max_length=14, unique=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='endereco', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
