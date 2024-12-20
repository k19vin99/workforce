# Generated by Django 5.1.3 on 2024-12-03 02:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestiones', '0005_customuser_genero'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='alergia_medicamento',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='contrato_adjunto',
            field=models.FileField(blank=True, null=True, upload_to='contratos/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='enfermedades',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='primer_apellido',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='primer_nombre',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='segundo_apellido',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='segundo_nombre',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='ContactoEmergencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=15)),
                ('parentesco', models.CharField(max_length=50)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contactos_emergencia', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
