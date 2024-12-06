# Generated by Django 5.1.3 on 2024-12-06 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestiones', '0008_customuser_segundo_apellido_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='certificado_afp',
            field=models.FileField(blank=True, null=True, upload_to='certificados/afp/', verbose_name='Certificado AFP'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='certificado_salud',
            field=models.FileField(blank=True, null=True, upload_to='certificados/salud/', verbose_name='Certificado de Salud'),
        ),
    ]
