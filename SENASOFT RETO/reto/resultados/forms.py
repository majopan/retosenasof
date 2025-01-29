from django import forms
from .models import CustomUser, Pacientes, OrdenLaboratorio, ResultadoPrueba, Response
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import admin

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('', 'Seleccione un rol'),
        ('admin', 'Admin'),
        ('medico', 'Médico'),
    ]
    
    TDOCUMENTO_CHOICES = [
        ('cedula_ciudadania', 'Cédula de ciudadanía'),
        ('tarjeta_identidad', 'Tarjeta de identidad'),
        ('cedula_extranjeria', 'Cédula de extranjería'),
    ]
    
    SEXO_CHOICES = [
        ('Femenino', 'Femenino'),
        ('Maculino', 'Maculino'),
        ('Otro', 'Otro'),
    ]

    # Campos del formulario
    codigo = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código único'}),
        label='Código único'
    )
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
        label='Nombre completo'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Correo electrónico', 'maxlength': '100'}),
        label='Correo electrónico'
    )
    direccion = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección de residencia'}),
        label='Dirección de residencia'
    )
    celular = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de celular'}),
        label='Número de celular'
    )
    tipo_identificacion = forms.ChoiceField(
        choices=TDOCUMENTO_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo de identificación'
    )
    numero_identificacion = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de identificación'}),
        label='Número de identificación'
    )
    fecha_nacimiento = forms.DateField(
        required=True,
        widget=forms.SelectDateWidget(years=range(1900, 2024), attrs={'class': 'form-control'}),
        label='Fecha de nacimiento'
    )
    sexo = forms.ChoiceField(
        choices=SEXO_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Sexo'
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Rol'
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        help_text=None
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Contraseña'}),
        help_text=None
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'codigo', 'name', 'email', 'direccion', 'celular', 'tipo_identificacion', 'numero_identificacion', 'fecha_nacimiento', 'sexo', 'role']
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
            'codigo': 'Código único',
            'name': 'Nombre completo',
            'email': 'Correo electrónico',
            'direccion': 'Dirección de residencia',
            'celular': 'Número de celular',
            'tipo_identificacion': 'Tipo de identificación',
            'numero_identificacion': 'Número de identificación',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'sexo': 'Sexo biológico',
            'role': 'Rol'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso. Por favor, elige otro.")
        return email

# Formulario para editar usuario
class modificarCustomUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['codigo', 'name', 'email', 'direccion', 'celular', 'tipo_identificacion', 'numero_identificacion', 'fecha_nacimiento', 'sexo', 'role']
        labels = {
            'codigo': 'Código único',
            'name': 'Nombre completo',
            'email': 'Correo electrónico',
            'direccion': 'Dirección de residencia',
            'celular': 'Número de celular',
            'tipo_identificacion': 'Tipo de identificación',
            'numero_identificacion': 'Número de identificación',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'sexo': 'Sexo biológico',
            'role': 'Rol'
        }
#Formulario de Pacientes
class formpaciente(forms.ModelForm):
    fechanacimiento = forms.DateField(
                    widget=forms.DateInput(attrs={
                        'class': 'form-control',
                        'type': 'date',  # Configura el campo como un selector de fechas
                        'placeholder': 'Fecha de Nacimiento (día/mes/año)'
                    })
                )
    class Meta :
        model = Pacientes
        fields = ['nombre','apellido1','apellido2','tpidentificacion','numeroidentificacion','fechanacimiento','sexo','direccion','telefono','correo', 'grupo_sanguineo']
        
        
class OrdenLaboratorioForm(forms.ModelForm):
    class Meta:
        model = OrdenLaboratorio
        fields = ['pacientes', 'fecha_orden', 'codigo_documento', 'numero_orden']
        widgets = {
            'fecha_orden': forms.DateInput(attrs={'type': 'date'}),
            'codigo_documento': forms.TextInput(attrs={'placeholder': 'Ingrese código de orden'}),
            'numero_orden': forms.TextInput(attrs={'placeholder': 'Ingrese número de orden'}),
        }
        
class ResultadoPruebaForm(forms.ModelForm):
    class Meta:
        model = ResultadoPrueba
        fields = ['orden_laboratorio', 'grupo_sanguineo', 'procedimiento', 'resultado']
        widgets = {
            'grupo_sanguineo': forms.Select(),
            'procedimiento': forms.TextInput(attrs={'placeholder': 'Ingrese procedimiento'}),
            'resultado': forms.TextInput(attrs={'placeholder': 'Ingrese resultado'}),
        }
        
        
# Formulario para chatbot


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
