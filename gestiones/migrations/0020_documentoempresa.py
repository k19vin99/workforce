# Generated by Django 5.1.2 on 2024-10-26 13:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestiones', '0019_liquidacion_año_liquidacion_mes'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentoEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('archivo', models.FileField(upload_to='documentos_empresa/')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('creado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
