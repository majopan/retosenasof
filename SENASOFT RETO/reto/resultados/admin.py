from django.contrib import admin
from .models import CustomUser,Pacientes, OrdenLaboratorio, ResultadoPrueba, Response
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Pacientes)
admin.site.register(OrdenLaboratorio)
admin.site.register(ResultadoPrueba)
