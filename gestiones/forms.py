from django import forms
import re
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import Group
from .models import Liquidacion, CargaFamiliar, CustomUser, Solicitud, Curso, Modulo, Comentario, Beneficio, Area, Denuncia, NotaDenuncia, EvidenciaDenuncia, Publicacion
from django.contrib.auth import get_user_model
from django.forms import modelformset_factory
import datetime

#Formulario de Registro de Usuario
class CustomUserCreationForm(UserCreationForm):
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Grupo")
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    email = forms.EmailField(required=True, label="Correo Electrónico")
    rut = forms.CharField(
        max_length=12,
        required=True,
        label="RUT",
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: 12345678-9',
            'class': 'form-control'
        })
    )
    area = forms.ModelChoiceField(queryset=Area.objects.all(), required=True, label="Área")
    fecha_contratacion = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        required=True, 
        label="Fecha de contratación"
    )
    telefono = forms.CharField(max_length=15, required=True, label="Número de Teléfono")
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        required=True, 
        label="Fecha de Nacimiento"
    )
    direccion = forms.CharField(max_length=255, required=True, label="Dirección")
    salud = forms.ChoiceField(choices=[
        ('fonasa', 'Fonasa'),
        ('banmedica', 'Banmédica'),
        ('colmena', 'Colmena Golden Cross'),
        ('consalud', 'Consalud'),
        ('cruzblanca', 'CruzBlanca'),
        ('esencial', 'Esencial'),
        ('masvida', 'Nueva Masvida'),
        ('vidatres', 'Vida Tres'),
    ], required=True, label="Plan de Salud")
    afp = forms.ChoiceField(choices=[
        ('capital', 'AFP Capital'),
        ('cuprum', 'AFP Cuprum'),
        ('habitat', 'AFP Habitat'),
        ('modelo', 'AFP Modelo'),
        ('planvital', 'AFP Planvital'),
        ('provida', 'AFP Provida'),
        ('uno', 'AFP Uno'),
    ], required=True, label="AFP")
    horario_asignado = forms.ChoiceField(choices=[
        ('8:00-17:30', '8:00 a 17:30'),
        ('9:00-18:30', '9:00 a 18:30'),
        ('21:00-8:00', '21:00 a 8:00'),
        ('otro', 'Otro'),
    ], required=True, label="Horario Asignado")
    cargo = forms.CharField(max_length=255, required=True, label="Cargo")

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 'rut', 'area', 'cargo', 
            'telefono', 'fecha_nacimiento', 'direccion', 'salud', 'afp', 'horario_asignado', 
            'fecha_contratacion', 'grupo', 'password1', 'password2'
        ]

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        # Verificar que el RUT ya esté registrado
        if CustomUser.objects.filter(rut=rut).exists():
            raise forms.ValidationError("El RUT ya está registrado.")
        # Verificar formato correcto (Ej: 12345678-9)
        rut_pattern = r'^\d{1,8}-[\dkK]$'
        if not re.match(rut_pattern, rut):
            raise forms.ValidationError("El formato del RUT no es válido. Debe ser en formato 12345678-9.")
        # Verificar dígito verificador
        if not self.validar_digito_verificador(rut):
            raise forms.ValidationError("El RUT ingresado no es válido.")
        return rut
    def validar_digito_verificador(self, rut):
        """Función para validar el dígito verificador de un RUT chileno."""
        try:
            rut_sin_dv, dv = rut.split('-')
            rut_sin_dv = int(rut_sin_dv)
            dv = dv.upper()
            suma = 0
            factor = 2
            for digit in reversed(str(rut_sin_dv)):
                suma += int(digit) * factor
                factor += 1
                if factor > 7:
                    factor = 2
            mod = 11 - (suma % 11)
            if mod == 11:
                dv_calculado = '0'
            elif mod == 10:
                dv_calculado = 'K'
            else:
                dv_calculado = str(mod)
            return dv == dv_calculado
        except:
            return False

class CustomUserChangeForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Grupo")
    area = forms.ModelChoiceField(queryset=Area.objects.all(), required=True, label="Área")
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        required=True, 
        label="Fecha de Nacimiento"
    )
    fecha_contratacion = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        required=True, 
        label="Fecha de Contratación"
    )
    rut = forms.CharField(
        max_length=12,
        required=True,
        label="RUT",
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: 12345678-9',
            'class': 'form-control'
        })
    )
    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 'rut', 'area', 'cargo', 
            'telefono', 'fecha_nacimiento', 'direccion', 'salud', 'afp', 'horario_asignado', 
            'fecha_contratacion', 'grupo'
        ]
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        # Verificar que el RUT ya esté registrado para otro usuario (pero no el actual)
        if CustomUser.objects.filter(rut=rut).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("El RUT ya está registrado por otro usuario.")
        # Verificar formato correcto (Ej: 12345678-9)
        rut_pattern = r'^\d{1,8}-[\dkK]$'
        if not re.match(rut_pattern, rut):
            raise forms.ValidationError("El formato del RUT no es válido. Debe ser en formato 12345678-9.")
        # Verificar dígito verificador
        if not self.validar_digito_verificador(rut):
            raise forms.ValidationError("El RUT ingresado no es válido.")
        return rut
    def validar_digito_verificador(self, rut):
        """ Función para validar el dígito verificador de un RUT chileno."""
        try:
            rut_sin_dv, dv = rut.split('-')
            rut_sin_dv = int(rut_sin_dv)
            dv = dv.upper()
            suma = 0
            factor = 2
            for digit in reversed(str(rut_sin_dv)):
                suma += int(digit) * factor
                factor += 1
                if factor > 7:
                    factor = 2
            mod = 11 - (suma % 11)
            if mod == 11:
                dv_calculado = '0'
            elif mod == 10:
                dv_calculado = 'K'
            else:
                dv_calculado = str(mod)
            return dv == dv_calculado
        except:
            return False
        
class LiquidacionSueldoForm(forms.ModelForm):
    class Meta:
        model = Liquidacion
        fields = ['usuario', 'sueldo_base', 'gratificacion', 'colacion', 'movilizacion', 'afp', 'salud', 'seguro_mutual', 'mes', 'año']
        widgets = {
            'mes': forms.Select(attrs={'class': 'form-control'}),
            'año': forms.NumberInput(attrs={'class': 'form-control', 'min': 2000, 'max': datetime.datetime.now().year + 1}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtiene el usuario desde kwargs
        super(LiquidacionSueldoForm, self).__init__(*args, **kwargs)
        if user and user.empresa:  # Verifica que el usuario y su empresa existan
            self.fields['usuario'].queryset = CustomUser.objects.filter(empresa=user.empresa)

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'cargo', 'telefono', 'fecha_nacimiento', 'area']  # Añadir 'area'

    # Definir un campo ModelChoiceField para mostrar las áreas disponibles como un dropdown
    area = forms.ModelChoiceField(queryset=Area.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        super(EditarUsuarioForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.empresa:
            # Filtrar las áreas por la empresa del colaborador
            self.fields['area'].queryset = Area.objects.filter(empresa=self.instance.empresa)

class CargaFamiliarForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control',  # Clase Bootstrap
            'style': 'max-width: 300px;'  # Limitar el ancho del campo
        }),
        label="Fecha de nacimiento",
        required=True
    )

    class Meta:
        model = CargaFamiliar
        fields = ['usuario', 'nombre', 'apellido', 'rut', 'parentesco', 'fecha_nacimiento']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CargaFamiliarForm, self).__init__(*args, **kwargs)
        if user and user.empresa:
            self.fields['usuario'].queryset = CustomUser.objects.filter(empresa=user.empresa)


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['tipo', 'descripcion', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ContactForm(forms.Form):
    MOTIVO_CONTACTO_CHOICES = [
        ('', 'Selecciona'),
        ('evaluar', 'Me interesa WorkForce para mi empresa'),
        ('soporte', 'Soy supervisor y necesito soporte'),
        ('oportunidades', 'Estoy buscando oportunidades laborales'),
    ]

    motivo_contacto = forms.ChoiceField(choices=MOTIVO_CONTACTO_CHOICES, required=True, label='¿Motivo de Contacto?')
    nombre = forms.CharField(max_length=100, required=True, label='Nombre')
    apellido = forms.CharField(max_length=100, required=True, label='Apellido')
    numero_telefono = forms.CharField(max_length=15, required=True, label='Número de teléfono')
    correo = forms.EmailField(required=True, label='Correo')
    nombre_empresa = forms.CharField(max_length=100, required=True, label='Nombre de la empresa')
    cantidad_colaboradores = forms.ChoiceField(choices=[('', 'Elije'), ('1-20', '1-20'), ('21-70', '21-70'), ('71-100', '71-100'), ('101+', '101+')], required=True, label='Cantidad de colaboradores')
    cargo = forms.CharField(max_length=100, required=True, label='Cargo')
    area_desempeno = forms.CharField(max_length=100, required=True, label='Área de desempeño')
    rubro = forms.CharField(max_length=100, required=True, label='Rubro')
    mensaje = forms.CharField(widget=forms.Textarea, required=False, label='¿En qué podemos ayudarte?')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'telefono', 'direccion', 'fecha_nacimiento', 'foto_perfil']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control shadow-sm'

class EditProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['foto_perfil']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']
        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class CursoForm(forms.ModelForm):
    participantes = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Participantes"
    )

    class Meta:
        model = Curso
        fields = ['nombre', 'descripcion', 'participantes']

    def __init__(self, *args, **kwargs):
        supervisor = kwargs.pop('supervisor', None)
        super(CursoForm, self).__init__(*args, **kwargs)
        if supervisor:
            # Filtra los participantes para que solo sean los colaboradores de la empresa del supervisor
            self.fields['participantes'].queryset = CustomUser.objects.filter(empresa=supervisor.empresa)


class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ['titulo', 'descripcion', 'archivo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario']


class EditarParticipantesForm(forms.ModelForm):
    participantes = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Participantes"
    )

    class Meta:
        model = Curso
        fields = ['participantes']

class BeneficioForm(forms.ModelForm):
    class Meta:
        model = Beneficio
        fields = ['titulo', 'descripcion', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['denunciado', 'motivo', 'descripcion', 'contacto_urgencia']  # Quitamos 'evidencias'
        labels = {
            'denunciado': 'Quiero denunciar a',
            'motivo': 'Motivo',
            'descripcion': 'Descripción',
            'contacto_urgencia': 'Datos de contacto para urgencias'
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }


class NotaDenunciaForm(forms.ModelForm):
    class Meta:
        model = NotaDenuncia
        fields = ['nota']
        labels = {
            'nota': '',  # Dejar vacío para no mostrar el label "Agregar Nota"
        }
        widgets = {
            'nota': forms.Textarea(attrs={
                'placeholder': 'Escribe aquí tu nota...', 
                'rows': 6,  # Puedes ajustar el número de filas según lo que necesites
                'class': 'form-control'  # Añadir la clase para estilos adicionales
            }),
        }

class EvidenciaDenunciaForm(forms.ModelForm):
    class Meta:
        model = EvidenciaDenuncia
        fields = ['archivo']
        labels = {
            'archivo': 'Evidencia',
        }

# Usamos modelformset para manejar múltiples archivos de evidencia
EvidenciaFormset = modelformset_factory(EvidenciaDenuncia, form=EvidenciaDenunciaForm, extra=3)

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'contenido', 'imagen']  # Incluye el campo de imagen
        labels = {
            'titulo': 'Título',
            'contenido': 'Descripción',
            'imagen': 'Imagen',
        }
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 4}),
        }