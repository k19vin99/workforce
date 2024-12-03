from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from datetime import date, timedelta
import holidays 

class Empresa(models.Model):
    nombre = models.CharField(max_length=255)
    razon_social = models.CharField(max_length=255)
    rut = models.CharField(max_length=12)
    giro = models.CharField(max_length=255)
    cantidad_personal = models.IntegerField()
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Area(models.Model):
    nombre = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='areas')

    def __str__(self):
        return f"{self.nombre} - {self.empresa.nombre}"
    
class CustomUser(AbstractUser):
    segundo_nombre = models.CharField(max_length=30, blank=True, null=True)
    segundo_apellido = models.CharField(max_length=30, blank=True, null=True)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)
    area = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True, blank=True)
    cargo = models.CharField(max_length=255, blank=True, null=True)
    fecha_contratacion = models.DateField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    GENERO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro'),
    ]
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES, null=True, blank=True)
    salud = models.CharField(max_length=30, choices=[
        ('fonasa', 'Fonasa'),
        ('banmedica', 'Banmédica'),
        ('colmena', 'Colmena Golden Cross'),
        ('consalud', 'Consalud'),
        ('cruzblanca', 'CruzBlanca'),
        ('esencial', 'Esencial'),
        ('masvida', 'Nueva Masvida'),
        ('vidatres', 'Vida Tres'),
    ], blank=True, null=True)
    afp = models.CharField(max_length=30, choices=[
        ('capital', 'AFP Capital'),
        ('cuprum', 'AFP Cuprum'),
        ('habitat', 'AFP Habitat'),
        ('modelo', 'AFP Modelo'),
        ('planvital', 'AFP Planvital'),
        ('provida', 'AFP Provida'),
        ('uno', 'AFP Uno'),
    ], blank=True, null=True)
    horario_asignado = models.CharField(max_length=20, choices=[
        ('8:00-17:30', '8:00 a 17:30'),
        ('9:00-18:30', '9:00 a 18:30'),
        ('21:00-8:00', '21:00 a 8:00'),
        ('otro', 'Otro'),
    ], null=True, blank=True)
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)
    @property
    def nombre_completo(self):
        """
        Retorna el nombre completo del usuario incluyendo segundo nombre y segundo apellido si están presentes.
        """
        nombres = [self.first_name, self.segundo_nombre, self.last_name, self.segundo_apellido]
        return " ".join(filter(None, nombres))

    def __str__(self):
        return self.username
    @property
    def dias_vacaciones_disponibles(self):
        """
        Calcula los días de vacaciones disponibles considerando:
        - 1.25 días hábiles por mes trabajado.
        - Desde la fecha de contratación.
        """
        if not self.fecha_contratacion:
            return 0

        today = date.today()
        # Calcular los meses trabajados
        meses_trabajados = (today.year - self.fecha_contratacion.year) * 12 + (today.month - self.fecha_contratacion.month)

        # Total acumulado según la ley chilena
        total_vacaciones = meses_trabajados * 1.25

        # Restar días ya usados en solicitudes aprobadas
        dias_usados = sum(
            solicitud.dias_habiles
            for solicitud in self.solicitudes_vacaciones.filter(estado='aprobada')
        )
        return max(0, total_vacaciones - dias_usados)

    def calcular_dias_habiles(self, fecha_inicio, fecha_fin):
        """
        Calcula la cantidad de días hábiles entre dos fechas dadas,
        excluyendo feriados en Chile.
        """
        chilean_holidays = holidays.CL(years=range(fecha_inicio.year, fecha_fin.year + 1))
        delta = (fecha_fin - fecha_inicio).days + 1
        return sum(
            1
            for day in (fecha_inicio + timedelta(days=i) for i in range(delta))
            if day.weekday() < 5 and day not in chilean_holidays
        )

    def __str__(self):
        return self.username

class ContactoEmergencia(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contactos_emergencia')
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    parentesco = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.parentesco})"
        
class CargaFamiliar(models.Model):
    TIPO_CERTIFICADO_CHOICES = [
        ('AFC', 'Certificado de Carga Familiar (AFC)'),
        ('ISAPRE', 'Certificado de Carga Familiar de la Isapre'),
        ('SUBSIDIOS', 'Certificado de Carga Familiar para Subsidios o Beneficios Sociales'),
        ('SII', 'Certificado de Carga Familiar del Servicio de Impuestos Internos (SII)'),
        ('REGISTRO_CIVIL', 'Certificados del Registro Civil'),
        ('OTRO', 'Otro'),
    ]
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    parentesco = models.CharField(max_length=50, choices=[
        ('hijo/a', 'Hijo/a'),
        ('esposo/a', 'Esposo/a'),
        ('padre/madre', 'Padre/Madre'),
        ('conviviente', 'Conviviente'),
        ('otro', 'Otro'),
    ])
    fecha_nacimiento = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cargas_familiares')
    
    tipo_certificado = models.CharField(max_length=20, choices=TIPO_CERTIFICADO_CHOICES, null=True, blank=True)
    archivo = models.FileField(upload_to='cargas_familiares/', null=True, blank=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.parentesco})'

class Asistencia(models.Model):
    colaborador = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora_entrada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.colaborador} - {self.fecha}"
    
class Solicitud(models.Model):
    TIPOS_SOLICITUD = [
        ('tramite', 'Permiso Trámite Personal'),
        ('administrativo', 'Día Administrativo'),
        ('cumpleanos', 'Descanso por Cumpleaños'),
        ('cumpleanos_hijo', 'Descanso por Cumpleaños Hijo/a'),
        ('otra', 'Otra'),
    ]

    ESTADO_SOLICITUD = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    colaborador = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=TIPOS_SOLICITUD)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=50, choices=ESTADO_SOLICITUD, default='pendiente')

    @property
    def dias_vacaciones(self):
        if self.tipo == 'vacaciones':
            antiguedad_meses = (date.today().year - self.colaborador.date_joined.year) * 12 + date.today().month - self.colaborador.date_joined.month
            return antiguedad_meses * 1.8
        return 0

    def __str__(self):
        return f"{self.colaborador.username} - {self.tipo}"

User = get_user_model()

class SolicitudVacaciones(models.Model):
    ESTADO_SOLICITUD = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    colaborador = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='solicitudes_vacaciones')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    dias_habiles = models.IntegerField(default=0) 
    estado = models.CharField(max_length=20, choices=ESTADO_SOLICITUD, default='pendiente')
    motivo = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def calcular_dias_habiles(self):
        chilean_holidays = holidays.CL(years=range(self.fecha_inicio.year, self.fecha_fin.year + 1))
        delta = (self.fecha_fin - self.fecha_inicio).days + 1
        return sum(
            1
            for day in (self.fecha_inicio + timedelta(days=i) for i in range(delta))
            if day.weekday() < 5 and day not in chilean_holidays
        )

    def save(self, *args, **kwargs):
        self.dias_habiles = self.calcular_dias_habiles()
        super().save(*args, **kwargs)

class Curso(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE)
    participantes = models.ManyToManyField(User, related_name='cursos')

    def __str__(self):
        return self.nombre

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="modulos")
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='modulos_archivos/', null=True, blank=True)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name="comentarios")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)  # Asegúrate de que timezone.now esté como default

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.modulo.titulo}"
    
class Beneficio(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='beneficios/', null=True, blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
    
class Denuncia(models.Model):
    ESTADOS_DENUNCIA = [
        ('pendiente', 'Pendiente'),
        ('revision', 'En Revisión'),
        ('resuelta', 'Resuelta'),
    ]
    denunciado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='denuncias_recibidas')
    denunciante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='denuncias_realizadas')
    motivo = models.CharField(max_length=255)
    descripcion = models.TextField()
    evidencias = models.FileField(upload_to='evidencias_denuncias/', null=True, blank=True)
    contacto_urgencia = models.CharField(max_length=100)
    estado = models.CharField(max_length=50, choices=ESTADOS_DENUNCIA, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField(null=True, blank=True)

    PRIORIDADES_DENUNCIA = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    prioridad = models.CharField(max_length=50, choices=PRIORIDADES_DENUNCIA, default='media')

    def __str__(self):
        return f"Denuncia de {self.denunciante} contra {self.denunciado}"
    
class NotaDenuncia(models.Model):
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE, related_name='notas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nota = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota de {self.usuario.username} - {self.denuncia.id}"
    
class HistorialDenuncia(models.Model):
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255)  # Ej: "Estado actualizado a resuelta"
    fecha = models.DateTimeField(auto_now_add=True)

class EvidenciaDenuncia(models.Model):
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE, related_name='evidencia_set')
    archivo = models.FileField(upload_to='evidencias_denuncias/')

class Publicacion(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='publicaciones/', null=True, blank=True)  # Campo para la imagen
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
    
class DocumentoEmpresa(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to='documentos_empresa/')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
class DescargaDocumento(models.Model):
    documento = models.ForeignKey(DocumentoEmpresa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_descarga = models.DateTimeField(auto_now_add=True)