# Generated by Django 5.1 on 2024-08-21 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestiones', '0002_alter_customuser_rut'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='direccion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='edad',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='horario_asignado',
            field=models.CharField(blank=True, choices=[('8:00-17:30', '8:00 a 17:30'), ('9:00-18:30', '9:00 a 18:30'), ('21:00-8:00', '21:00 a 8:00'), ('otro', 'Otro')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='salud',
            field=models.CharField(choices=[('fonasa', 'Fonasa'), ('banmedica', 'Banmédica'), ('colmena', 'Colmena Golden Cross'), ('consalud', 'Consalud'), ('cruzblanca', 'CruzBlanca'), ('esencial', 'Esencial'), ('masvida', 'Nueva Masvida'), ('vidatres', 'Vida Tres')], default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
