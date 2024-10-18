# Generated by Django 5.1 on 2024-10-15 18:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestiones', '0013_area_customuser_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='Denuncia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('evidencias', models.FileField(blank=True, null=True, upload_to='evidencias_denuncias/')),
                ('contacto_urgencia', models.CharField(max_length=100)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('denunciado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='denuncias_recibidas', to=settings.AUTH_USER_MODEL)),
                ('denunciante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='denuncias_realizadas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]