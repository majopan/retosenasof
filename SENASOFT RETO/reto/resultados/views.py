from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login , logout as auth_logout
from django.db import IntegrityError
from .models import CustomUser, Pacientes, OrdenLaboratorio, ResultadoPrueba, Response
from .forms import CustomUserCreationForm, modificarCustomUserForm, formpaciente, OrdenLaboratorioForm, ResultadoPruebaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
import datetime
from django.shortcuts import render
from django.http import JsonResponse,  FileResponse
from .models import Response
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
# enviar mensajes de gmail
import os

from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
# conversion pdf
from reportlab.pdfgen import canvas
from django.urls import reverse
from django.core.paginator import Paginator



def email(correo,mensaje):
    load_dotenv()

    email_sender="panzzz956@gmail.com"
    password=os.getenv("PASSWORD")
    email_reciver=correo

    subject ="ordenes medicas"
    body=f"""
    {mensaje}
    mensaje enviado desde python {email_sender}
    """

    em=EmailMessage()
    em["From"] = email_sender
    em["To"] = email_reciver
    em["Subject"]=subject
    em.set_content(body)

    context =ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp:
        smtp.login(email_sender,password)
        smtp.sendmail(email_sender,email_reciver,em.as_string())
    return




def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            # Verifica si las contraseñas coinciden
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    # Guarda el usuario usando el formulario
                    user = form.save()
                    # Inicia sesión automáticamente
                    login(request, user)
                    # Redirige a la vista deseada después del registro
                    return redirect('mostrar_user')  # Cambia 'principal' al nombre de tu vista de inicio
                except IntegrityError:
                    return render(request, 'registrouser.html', {
                        'form': form,
                        'error': "Error al crear el usuario. Por favor, inténtalo de nuevo."
                    })
            else:
                return render(request, 'registrouser.html', {
                    'form': form,
                    'error': "Las contraseñas no coinciden."
                })
        else:
            return render(request, 'registrouser.html', {
                'form': form,
                'error': "Hay errores en la información ingresada. Por favor, revisa los campos."
            })
    else:
        form = CustomUserCreationForm()
        mytitle = "Registro Nuevos Usuarios"
        return render(request, 'registrouser.html', {
            'title': mytitle,
            'form': form
        })







def principal(request):
    return render(request, 'principal.html')





#vista para crear la tabla de mostrar users

def mostrar_user(request):
    users = CustomUser.objects.all()  # Obtiene todos los usuarios
    return render(request, 'mostrar_user.html', {
        'users': users
    })
    
    





#vista editar user

def editar_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = modificarCustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('mostrar_user')  # Redirige a la lista de usuarios después de editar
    else:
        form = modificarCustomUserForm(instance=user)
    
    return render(request, 'editar_user.html', {
        'form': form,
        'user': user
    })






def eliminar_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('mostrar_user')  # Redirige a la lista de usuarios después de eliminar

    return render(request, 'eliminar_user.html', {
        'user': user
    })






#login user

#login
def loginzzz(request):
    if request.method == "GET":
        return render(request,'login.html',{
            'form' : AuthenticationForm
        })
        
#funciones para el login
    else:
        user = authenticate(request, username= request.POST['username']
                            ,password=request.POST["password"])
        #verificacion de contraseña para el usuario
        if user is None:
            return render(request, 'login.html', {
                "form" : AuthenticationForm,
                'error': 'El usuario o la contraseña es incorrecto'
            })
        else:
            login(request, user)
            #enviar_email(user.email)
            return redirect('mostrar_user')








#cierre de sesion de users
#cerrar sesion
def logout(request):
    auth_logout(request)  # Llama a la función de logout proporcionada por Django
    return redirect('paciente_login')  # Redirige al usuario a la página de login






#Vista de Pacientes

def Persona(request):
    if request.method == 'GET':
        return render(request, 'vpaciente.html',{
            'vista' : formpaciente
        })
    else:
        try:
            form=formpaciente(request.POST)
            form.save() 
            return redirect('mostrarpaciente')
        except ValueError:
            return render(request, 'vpaciente.html',{
                'mal': 'Debes registrar un Paciente'
            })

            
#mostrar los paciente

def mospaciente(request):
    if request.method == 'GET':
        pq = Pacientes.objects.all()
        return render(request, 'mospaciente.html', {
            'verpaciente': pq
        })



# Vista para el login del paciente
def paciente_login(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        tpidentificacion = request.POST.get('tpidentificacion')
        numeroidentificacion = request.POST.get('numeroidentificacion')
        fechanacimiento = request.POST.get('fechanacimiento')

        # Verificar hCaptcha
        hcaptcha_response = request.POST.get('h-captcha-response')
        data = {
            'secret': settings.HCAPTCHA_SECRET_KEY,  # El secreto de hCaptcha
            'response': hcaptcha_response
        }
        r = requests.post('https://hcaptcha.com/siteverify', data=data)
        result = r.json()

        if result['success']:
            # Intentar autenticar al paciente si hCaptcha es exitoso
            try:
                paciente = Pacientes.objects.get(
                    tpidentificacion=tpidentificacion,
                    numeroidentificacion=numeroidentificacion,
                    fechanacimiento=fechanacimiento
                )
                # Si el paciente es encontrado, guardar su ID en la sesión
                request.session['paciente_id'] = paciente.id
                messages.success(request, f'¡Bienvenido/a {paciente.nombre}!')
                return redirect('aceptar_politica')  # Redirigir al dashboard de pacientes
            except Pacientes.DoesNotExist:
                # Si el paciente no existe, mostrar mensaje de error
                messages.error(request, 'Identificación o fecha de nacimiento incorrectos.')
        else:
            # Si hCaptcha falla
            messages.error(request, 'La validación de hCaptcha falló. Inténtalo de nuevo.')

    # Mostrar la página de inicio de sesión
    return render(request, 'paciente_login.html')


# Vista del dashboard del paciente

def dashboard_paciente(request):
    # Obtener el paciente autenticado por su ID guardado en la sesión
    paciente_id = request.session.get('paciente_id')
    if not paciente_id:
        messages.error(request, 'Por favor inicia sesión.')
        return redirect('paciente_login')

    # Buscar el paciente en la base de datos
    paciente = Pacientes.objects.get(id=paciente_id)
    
    # Renderizar el dashboard con los datos del paciente
    return render(request, 'dashboard_paciente.html', {'paciente': paciente})


def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Pacientes, id=paciente_id)  # Obtener el paciente por ID

    if request.method == 'GET':
        form = formpaciente(instance=paciente)  # Prepopulamos el formulario con los datos del paciente
        return render(request, 'vpaciente.html', {
            'vista': form,
            'paciente': paciente  # Pasar el paciente para usar en la plantilla si es necesario
        })
    else:
        try:
            form = formpaciente(request.POST, instance=paciente)  # Asegúrate de usar la instancia
            form.save()  # Guardar los cambios
            return redirect('mostrarpaciente')  # Redirigir a la vista que muestra la lista de pacientes
        except ValueError:
            return render(request, 'vpaciente.html', {
                'mal': 'Debes actualizar el Paciente'
            })
            
            


def eliminar_paciente(request, paciente_id):
    paciente = get_object_or_404(Pacientes, id=paciente_id)  # Obtener el paciente por ID

    if request.method == 'POST':
        paciente.delete()  # Eliminar el paciente
        return redirect('mostrarpaciente')  # Redirigir a la lista de pacientes



def mostrar_ordenes(request):
    pacientes = request.session.get('paciente_id', None)
    if not pacientes:
        return redirect('crear_orden') 
    
    paci = Pacientes.objects.get(id=pacientes)
    ordenes = OrdenLaboratorio.objects.filter(pacientes=paci)

    # Paginación
    paginator = Paginator(ordenes, 10)  # Muestra 10 órdenes por página
    page_number = request.GET.get('page')  # Obtener el número de página de la solicitud
    page_obj = paginator.get_page(page_number)  # Obtener las órdenes de la página actual

    return render(request, 'or.html', {
        'page_obj': page_obj,
        'paciente': paci  # Pasar el paciente actual para usar en la plantilla si es necesario
    })


#Vista de Formulario de Ordenes

def crear_orden(request):
    if request.method == 'POST':
        form = OrdenLaboratorioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Orden de laboratorio creada exitosamente.')
            return redirect('mostrar_ordenes')
    else:
        form = OrdenLaboratorioForm()

    return render(request, 'crear_orden.html', {'form': form})



# VISTA MOSTRAR ORDEN_FILTROS

def mostrar_ordenes_filtro(request):
    pacientes_id = request.session.get('paciente_id')
    if not pacientes_id:
        return JsonResponse({'error': 'No hay paciente seleccionado'}, status=400)
    
    paciente = Pacientes.objects.get(id=pacientes_id)
    ordenes = OrdenLaboratorio.objects.filter(pacientes=paciente)

    # Filtrar por número de orden si está presente
    numero_orden = request.GET.get('numero_orden')
    if numero_orden:
        ordenes = ordenes.filter(numero_orden=numero_orden)
    
    # Filtrar por rango de fecha
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    if fecha_inicio and fecha_fin:
        fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fecha_fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        ordenes = ordenes.filter(fecha_orden__range=(fecha_inicio, fecha_fin))
    
    # Ordenar por fecha ascendente o descendente
    orden_fecha = request.GET.get('orden_fecha', 'asc')  # El valor predeterminado es 'asc'
    if orden_fecha == 'asc':
        ordenes = ordenes.order_by('fecha_orden')
    else:
        ordenes = ordenes.order_by('-fecha_orden')

    # Preparar datos para la respuesta
    data = [{
        'fecha_orden': orden.fecha_orden.strftime('%Y-%m-%d'),
        'codigo_documento': orden.codigo_documento,
        'numero_orden': orden.numero_orden,
        'id': orden.id  # Añadir el ID de la orden para usarlo en la vista
    } for orden in ordenes]
    
    return JsonResponse(data, safe=False)





# VISTA MOSTRAR RESULTADO

def mostrar_resultados(request, orden_id):
    # Obtener la orden de laboratorio
    orden = get_object_or_404(OrdenLaboratorio, id=orden_id)

    # Filtrar los resultados asociados con esta orden
    resultados = ResultadoPrueba.objects.filter(orden_laboratorio=orden)

    # Pasar la orden y los resultados a la plantilla
    return render(request, 'resultadosprueba.html', {
        'resultados': resultados,
        'orden': orden  # Información de la orden para mostrar detalles en la plantilla
    })

    
    
    
def crear_resultado(request):
    if request.method == 'POST':
        form = ResultadoPruebaForm(request.POST)
        if form.is_valid():
            form.save()  # Ahora el formulario se encarga de guardar el resultado junto con la orden
            messages.success(request, 'Resultado de prueba creado exitosamente.')
            return redirect('mostrar_ordenes')
    else:
        form = ResultadoPruebaForm()

    return render(request, 'crear_resultado.html', {'form': form})

    
def generar_pdf_view(request, paciente_id, orden_id):
    # Obtén el paciente y la orden
    paciente = get_object_or_404(Pacientes, id=paciente_id)
    orden = get_object_or_404(OrdenLaboratorio, id=orden_id)
    
    # Crear el archivo de respuesta HTTP para el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orden_{paciente.numeroidentificacion}.pdf"'
    
    # Crear el PDF usando reportlab
    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, f"Paciente: {paciente.nombre} {paciente.apellido1}")
    p.drawString(100, 780, f"Identificación: {paciente.numeroidentificacion}")
    p.drawString(100, 760, f"Email: {paciente.correo}")
    p.drawString(100, 740, f"Última Orden de Laboratorio:")
    p.drawString(100, 720, f"Código de la orden: {orden.numero_orden}")
    p.drawString(100, 700, f"Fecha de la orden: {orden.fecha_orden}")

    # Finalizar el PDF
    p.showPage()
    p.save()
    
    return response




PREDEFINED_RESPONSES = {
    "hola": "¡Hola! ¿Cómo te puedo ayudar? Si necesitas agendar una cita o saber más sobre nuestros servicios, solo pregunta.",
    "adiós": "¡Adiós! Que tengas un buen día.",
    "¿cómo estás?": "¡Estoy bien, gracias por preguntar! ¿Te gustaría agendar una cita?",
    "horarios": "Nuestros horarios de atención son de lunes a viernes, de 8:00 AM a 6:00 PM.",
    "cita": "Para agendar una cita, por favor proporciona tu número de cédula para buscar tu información.",
    "servicios": "Ofrecemos consultas generales, especialidades médicas y chequeos preventivos. ¿Te gustaría más información sobre algún servicio específico?"
}

def chatbot_view(request):
    if request.method == 'POST':
        question = request.POST.get('question', '').lower()

        if question.isdigit():
            paciente = Pacientes.objects.filter(numeroidentificacion=question).first()
            if paciente:
                pa = get_object_or_404(Pacientes, pk=paciente.id)
                ordenLab = OrdenLaboratorio.objects.filter(pacientes=pa).order_by('-fecha_orden').first()

                if ordenLab:
                    # Generar la URL completa para descargar el PDF
                    pdf_url = request.build_absolute_uri(reverse('descargar_pdf', args=[paciente.id, ordenLab.id]))
                    # Generar la respuesta con un hipervínculo HTML
                    answer = (f"Paciente encontrado: {paciente.nombre} {paciente.apellido1}, "
                            f"tu email es {paciente.correo}, y tu última cita fue el {ordenLab.fecha_orden}. "
                            f"¿Te gustaría agendar una nueva cita o <a href=\"{pdf_url}\" target=\"_blank\">descargar tu orden más reciente en PDF</a>?")
                    email(paciente.correo, answer)
                else:
                    answer = "Paciente encontrado, pero no tienes órdenes de laboratorio registradas. ¿Te gustaría agendar una cita?"

            else:
                answer = "No se encontró ningún paciente con esa cédula. ¿Te gustaría registrarte como nuevo paciente?"

        else:
            answer = PREDEFINED_RESPONSES.get(question, "Lo siento, no entiendo la pregunta. ¿Te gustaría hablar con un asesor?")

        return JsonResponse({'answer': answer})

    return render(request, 'bot/chatbot.html')



#Politica de Tratamiento de Datos

def aceptar_politica(request):
    return render(request, 'tratamiento_datos.html')


#Vista Menu
def menu(request):
    return render(request, 'navegacion.html')





def mostrar_pacientes_medico(request):
    # Lógica para obtener los pacientes del médico
    return render(request, 'nombre_del_template.html', {'pacientes': Pacientes})