from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import joblib
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.generic import TemplateView
import numpy as np

# Create your views here

class PrediccionAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'EDUCACION_MADRE': openapi.Schema(type=openapi.TYPE_INTEGER),
                'EDUCACION_PADRE': openapi.Schema(type=openapi.TYPE_INTEGER),
                'TIENE_COMPUTADOR': openapi.Schema(type=openapi.TYPE_INTEGER),
                'TIENE_INTERNET': openapi.Schema(type=openapi.TYPE_INTEGER),
                'ESTRATO_VIVIENDA': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['EDUCACION_MADRE', 'EDUCACION_PADRE', 'TIENE_COMPUTADOR', 'TIENE_INTERNET', 'ESTRATO_VIVIENDA']
        ),
        responses={
            200: openapi.Response('Respuesta exitosa', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            405: 'Método no permitido'
        }
    )
    @csrf_exempt
    def post(self, request):
        # Obtener los datos de entrada desde el cuerpo de la solicitud POST
        EDUCACION_MADRE = int(request.data.get('EDUCACION_MADRE'))
        EDUCACION_PADRE = int(request.data.get('EDUCACION_PADRE'))
        TIENE_COMPUTADOR = int(request.data.get('TIENE_COMPUTADOR'))
        TIENE_INTERNET = int(request.data.get('TIENE_INTERNET'))
        ESTRATO_VIVIENDA = int(request.data.get('ESTRATO_VIVIENDA'))

            # Cargar el modelo desde el archivo
        modelo_prediccion = joblib.load('modelo_prediccion.pkl')
        # Crear el array de entrada con los datos de prueba
        datos_entrada = np.array([EDUCACION_MADRE, EDUCACION_PADRE, TIENE_COMPUTADOR, TIENE_INTERNET, ESTRATO_VIVIENDA])

        # Reshape del array de entrada
        datos_entrada_reshaped = datos_entrada.reshape(1, -1)

        # Hacer la predicción utilizando el modelo cargado y los datos de entrada
        prediccion = modelo_prediccion.predict(datos_entrada_reshaped)
        # Generar mensajes de consejo en función del valor de la predicción
        if prediccion < 230:
            mensaje_consejo = "¡Tu puntaje es bastante bajo! Te recomendamos estudiar más y practicar ejercicios similares para mejorar tus habilidades en las áreas evaluadas."
        elif prediccion >=230 and prediccion<250:
            mensaje_consejo = "Tu puntaje es bajo. Te sugerimos dedicar tiempo a repasar los temas que consideres más débiles y realizar simulacros de las pruebas para familiarizarte con el formato y agilizar tus respuestas."
        elif prediccion >=250 and prediccion<300:
            mensaje_consejo = "Tu puntaje es promedio. Puedes enfocarte en reforzar aquellos temas que sientas menos dominados y practicar la resolución de ejercicios adicionales para aumentar tu velocidad y precisión."
        elif prediccion >=300 and prediccion<370:
            mensaje_consejo = "Tienes un buen puntaje. Sin embargo, siempre es recomendable seguir practicando y resolviendo ejercicios para mantener tus habilidades afiladas y asegurar un mejor desempeño en las pruebas."
        elif prediccion >=370:
            mensaje_consejo = "¡Felicitaciones! Tu puntaje es excelente. Continúa repasando los temas para mantener tu nivel y considera compartir tus técnicas de estudio con otros estudiantes."


        # Retornar la respuesta como JSON
        return Response({'Prediccion Puntaje': int(prediccion), 'msg':mensaje_consejo })

def PrediccionTemplateAPIView(request):

    if  request.method == 'POST':

        EDUCACION_MADRE = request.POST.get('parametro1')
        EDUCACION_PADRE = request.POST.get('parametro2')
        TIENE_INTERNET = request.POST.get('parametro3')
        TIENE_COMPUTADOR = request.POST.get('parametro4')
        ESTRATO_VIVIENDA = request.POST.get('parametro5')

        print('EDUCACION_MADRE:', EDUCACION_MADRE)
        print('EDUCACION_PADRE:', EDUCACION_PADRE)
        print('TIENE_INTERNET:', TIENE_INTERNET)
        print('TIENE_COMPUTADOR:', TIENE_COMPUTADOR)
        print('ESTRATO_VIVIENDA:', ESTRATO_VIVIENDA)
        modelo_prediccion = joblib.load('modelo_prediccion.pkl')
        # Crear el array de entrada con los datos de prueba
        datos_entrada = np.array([EDUCACION_MADRE, EDUCACION_PADRE, TIENE_COMPUTADOR, TIENE_INTERNET, ESTRATO_VIVIENDA])

        # Reshape del array de entrada
        datos_entrada_reshaped = datos_entrada.reshape(1, -1)

        # Hacer la predicción utilizando el modelo cargado y los datos de entrada
        prediccion = modelo_prediccion.predict(datos_entrada_reshaped)
        print('prediccion ',prediccion)
        # Generar mensajes de consejo en función del valor de la predicción
        if prediccion < 230:
            mensaje_consejo = "¡Tu puntaje es bastante bajo! Te recomendamos estudiar más y practicar ejercicios similares para mejorar tus habilidades en las áreas evaluadas."
        elif prediccion >=230 and prediccion<250:
            mensaje_consejo = "Tu puntaje es bajo. Te sugerimos dedicar tiempo a repasar los temas que consideres más débiles y realizar simulacros de las pruebas para familiarizarte con el formato y agilizar tus respuestas."
        elif prediccion >=250 and prediccion<300:
            mensaje_consejo = "Tu puntaje es promedio. Puedes enfocarte en reforzar aquellos temas que sientas menos dominados y practicar la resolución de ejercicios adicionales para aumentar tu velocidad y precisión."
        elif prediccion >=300 and prediccion<370:
            mensaje_consejo = "Tienes un buen puntaje. Sin embargo, siempre es recomendable seguir practicando y resolviendo ejercicios para mantener tus habilidades afiladas y asegurar un mejor desempeño en las pruebas."
        elif prediccion >=370:
            mensaje_consejo = "¡Felicitaciones! Tu puntaje es excelente. Continúa repasando los temas para mantener tu nivel y considera compartir tus técnicas de estudio con otros estudiantes."

        context = {
            'puntaje': int(prediccion),
            'msg': mensaje_consejo,
        }
        return render(request, "index.html", context)
    
    return render(request, "index.html")

    

