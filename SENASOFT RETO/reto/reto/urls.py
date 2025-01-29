"""
URL configuration for reto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from resultados import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de autenticación
    path('login/', views.loginzzz, name='loginzzz'),
    path('logout/', views.logout, name='logout'),
    path('registro/', views.registro, name='registro'),
    
    # Rutas del perfil y dashboard del paciente
    path('principal/', views.principal, name='principal'),
    path('mostrar_user/', views.mostrar_user, name='mostrar_user'),
    path('editar_user/<int:user_id>/', views.editar_user, name='editar_user'),
    path('eliminar_user/<int:user_id>/', views.eliminar_user, name='eliminar_user'),
    
    # Rutas de pacientes
    path('mostrarpaciente/', views.mospaciente, name='mostrarpaciente'),
    path('paciente/', views.Persona, name='paciente'),
    path('', views.paciente_login, name='paciente_login'),
    path('pacientedashboard/', views.dashboard_paciente, name='dashboard_paciente'),
    path('pacientes/editar/<int:paciente_id>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/eliminar/<int:paciente_id>/', views.eliminar_paciente, name='eliminar_paciente'),


    # Rutas de órdenes de laboratorio
        path('ordenes/', views.mostrar_ordenes, name='mostrar_ordenes'),
    path('ordenes/filtrar/', views.mostrar_ordenes_filtro, name='filtrar_ordenes'),
    path('resultados/<int:orden_id>/', views.mostrar_resultados, name='mostrar_resultados'),
    path('crear-orden/', views.crear_orden, name='crear_orden'),
    path('crear-resultado/', views.crear_resultado, name='crear_resultado'),
    

    #generar pdf - chatboot
    path('descargar-pdf/<int:paciente_id>/<int:orden_id>/', views.generar_pdf_view, name='descargar_pdf'),

    # Ruta para el chatbot
    path('chatbot/', views.chatbot_view, name='chatbot_view'),

    # Ruta para aceptar política de datos
    path('aceptar-politica/', views.aceptar_politica, name='aceptar_politica'),

    # Ruta para el menú
    path('menu/', views.menu, name='men'),
    
    path('mostrar_pacientes_medico/', views.mostrar_pacientes_medico, name='mostrar_pacientes_medico'),
]
