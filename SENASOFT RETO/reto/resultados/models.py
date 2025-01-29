from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('', 'Seleccione un rol'),
        ('admin', 'Admin'),
        ('medico', 'Medico'),
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

    codigo = models.CharField(max_length=255, verbose_name='código único')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='')
    name = models.CharField(max_length=255, verbose_name='Nombre completo')
    email = models.EmailField(verbose_name='Correo electrónico')
    direccion = models.CharField(max_length=255, verbose_name='Dirección de residencia')
    celular = models.CharField(max_length=15, verbose_name='Número de celular')
    tipo_identificacion = models.CharField(max_length=20, choices=TDOCUMENTO_CHOICES, verbose_name='Tipo de identificación')
    numero_identificacion = models.CharField(max_length=20, verbose_name='Número de identificación')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento', null=True, blank=True)  # Campo no nulo
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, verbose_name='Sexo biológico')

    # Relaciones ManyToMany
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='Los grupos a los que pertenece este usuario. El usuario obtendrá todos los permisos otorgados a cada uno de sus grupos.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Permisos específicos para este usuario.',
        related_query_name='customuser',
    )
#Modelo de Pacientes
class Pacientes(models.Model):
    TIPOIDENTIFICACIÓN_CHOICES = [
        ('', 'Seleccione un el tipo de Identificación'),
        ('CC', 'Cedula de Ciudadania'),
        ('CE', 'Cedula de Extrangeria'),
        ('TI', 'Tarjeta de Identidad'),
        ('RC', 'Registro Civil'),
        ('P', 'Pasaporte'),
    ]
    SEXO_CHOICES = [
        ('Femenino', 'Femenino'),
        ('Maculino', 'Maculino'),
        ('Otro', 'Otro'),
    ]
    
    TIPOSANGRE_CHOICES=[#Select
        ('A+','A+'),
        ('A-','A-'),
        ('O+','O+'),
        ('O-','O-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('B+','B+'),
        ('B-','B-')]
    nombre = models.CharField(max_length=255)#valor en texto
    apellido1 = models.CharField(max_length=255)
    apellido2 = models.CharField(max_length=255, blank=True)
    tpidentificacion = models.CharField(max_length=10, choices=TIPOIDENTIFICACIÓN_CHOICES, default='')
    numeroidentificacion = models.CharField(max_length=50)
    fechanacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, verbose_name='Sexo biológico')
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    grupo_sanguineo = models.CharField(max_length=100, choices=TIPOSANGRE_CHOICES)

    #muestre informacion
    def __str__(self):
        return self.nombre + ' Identificación ' + self.numeroidentificacion
    
    
class OrdenLaboratorio(models.Model):
    pacientes = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    fecha_orden = models.DateField()
    codigo_documento = models.CharField(max_length=100)
    numero_orden = models.CharField(max_length=20)

    class Meta:
        ordering = ['-fecha_orden']  # Ordenar de forma descendente por fecha de manera predeterminada

    def __str__(self):
        return f"Orden {self.numero_orden} - {self.fecha_orden}"


class ResultadoPrueba(models.Model):
    TIPOSANGRE_CHOICES=[#Select
        ('A+','A+'),
        ('A-','A-'),
        ('O+','O+'),
        ('O-','O-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('B+','B+'),
        ('B-','B-')]
    orden_laboratorio = models.ForeignKey(OrdenLaboratorio, related_name='resultados', on_delete=models.CASCADE)
    grupo_sanguineo = models.CharField(max_length=100, choices=TIPOSANGRE_CHOICES)
    procedimiento = models.CharField(max_length=100)
    resultado = models.CharField(max_length=100)
    fecha_resultado = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.procedimiento} - {self.resultado}"


#esto es para lo del chatbot
class Response(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
