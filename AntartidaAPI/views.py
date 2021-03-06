from datetime import date
import datetime
from io import StringIO
from django.db.models.fields import CharField, DateTimeField, EmailField
from rest_framework import response,status,generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from AntartidaFront.models import *
from .serializers import *
import logging
import json
from django.core.mail import send_mail
# Utilizando los genericos de DRF crea automaticamente los controllers(llamados views en django)


@api_view(['GET', 'POST'])

def sensor_view(request):
    if(request.method == 'GET'):
        sensores = Sensor.sensores_objects.all()
        sensores_serializer = SensorSerializer(sensores, many=True)
        return Response(sensores_serializer.data)

    elif(request.method == 'POST'):
        if (request.POST.get('nombre_sensor')): 
            try:   
                sensor = Sensor.objects.get(nombre=request.POST.get('nombre_sensor'))
            except:
                sensor = Sensor.objects.create(nombre=request.POST.get('nombre_sensor'))
            lectura = Lectura.objects.create(sensor_id = sensor.id, fecha_lectura = request.POST.get('fecha_lectura'))
            mediciones= json.loads(request.POST.get('lectura'))
            
            for medicion in mediciones:
                try:
                    tipo_medicion = TipoMedicion.objects.get(nombre=medicion['tipo'])
                    medicion = Medicion.objects.create(lectura_id = lectura.id, tipo_medicion_id=tipo_medicion.id,valor=medicion['valor'])
                except:
                    print('OMAR ALGO ANDA MAL')
            return Response({}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def sensor_detail_view(request,id=None):

    if request.method == 'GET':
        sensor = Sensor.sensores_objects.filter(id=id).first()
        sensor_serializer = SensorSerializer(sensor)
        return Response(sensor_serializer.data)

    elif request.method == 'PUT':
        sensor = Sensor.sensores_objects.filter(id=id).first()
        sensor_serializer = SensorSerializer(sensor, data=request.data)
        if sensor_serializer.is_valid():
            sensor_serializer.save()
            return Response(sensor_serializer.data)
        return Response(sensor_serializer.error_messages)

    elif request.method == 'DELETE':
        sensor: Sensor = Sensor.objects.filter(id=id).first()
        sensor.delete()
        return Response('Eliminado con ??xito')
    
@api_view(['DELETE'])
def sensor_delete_view(request,id=None):
    if request.method == 'DELETE':
        sensor: Sensor = Sensor.sensores_objects.filter(id=id).first()
        sensor.deleted = True
        sensor.save()
        return Response("Eliminado exitosamente")

@api_view(['GET'])
def usuario_view(request):
    if(request.method == 'GET'):
        usuarios = Usuario.usuarios_objects.all()
        usuarios_serializer = UsuarioSerializer(usuarios, many=True)
        return Response(usuarios_serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def usuario_detail_view(request,id=None):

    if request.method == 'GET':
        usuario = Usuario.objects.filter(id=id).first()
        usuario_serializer = UsuarioSerializer(usuario)
        return Response(usuario_serializer.data)

    elif request.method == 'PUT':
        usuario = Usuario.objects.filter(id=id).first()
        usuario_serializer = UsuarioSerializer(usuario, data=request.data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return Response(usuario_serializer.data)
        return Response(usuario_serializer.error_messages)

    elif request.method == 'DELETE':
        usuario = Usuario.objects.filter(id=id).first()
        usuario.delete()
        return Response('Eliminado con ??xito')

@api_view(['GET'])
def lectura_view(request,sensor=None):
    if(request.method == 'GET'):
        lecturas = Lectura.lecturas_objects.filter(sensor=sensor)
        lecturas_serializer = LecturaSerializer(lecturas, many=True)
        return Response(lecturas_serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def lectura_detail_view(request,id=None):

    if request.method == 'GET':
        lectura = Lectura.objects.filter(id=id).first()
        lectura_serializer = LecturaSerializer(lectura)
        return Response(lectura_serializer.data)

    elif request.method == 'PUT':
        lectura = Lectura.objects.filter(id=id).first()
        lectura_serializer = LecturaSerializer(lectura, data=request.data)
        if lectura_serializer.is_valid():
            lectura_serializer.save()
            return Response(lectura_serializer.data)
        return Response(lectura_serializer.error_messages)

    elif request.method == 'DELETE':
        lectura = Lectura.objects.filter(id=id).first()
        lectura.delete()
        return Response('Eliminado con ??xito')


@api_view(['GET'])
def medicion_view(request):
    if(request.method == 'GET'):
        mediciones = Medicion.mediciones_objects.all()
        mediciones_serializer = MedicionSerializer(mediciones, many=True)
        return Response(mediciones_serializer.data)
    

@api_view(['GET', 'PUT', 'DELETE'])
def medicion_detail_view(request,id=None):

    if request.method == 'GET':
        medicion = Medicion.mediciones_objects.filter(id=id).first()
        medicion_serializer = MedicionSerializer(medicion)
        return Response(medicion_serializer.data)

    elif request.method == 'PUT':
        medicion = Medicion.mediciones_objects.filter(id=id).first()
        medicion_serializer = MedicionSerializer(medicion, data=request.data)
        if medicion_serializer.is_valid():
            medicion_serializer.save()
            return Response(medicion_serializer.data)
        return Response(medicion_serializer.error_messages)


    elif request.method == 'DELETE':
        medicion = Medicion.mediciones_objects.filter(id=id).first()
        medicion.delete()
        return Response('Eliminado con ??xito')
    
    
@api_view(['GET'])
def tipo_medicion_view(request):
    if(request.method == 'GET'):
        tipo_mediciones = TipoMedicion.tipo_mediciones_objects.all()
        tipo_mediciones_serializer = TipoMedicionSerializer(tipo_mediciones, many=True)
        return Response(tipo_mediciones_serializer.data)
    

@api_view(['GET'])
def sensor_lecturas_por_fecha_view(request,sensor=None):
    if(request.method == 'GET'):
        lecturas = Lectura.lecturas_objects.filter(sensor=sensor,fecha_lectura__lte=request.GET.get('hasta', '') +" 23:59:59",fecha_lectura__gte=request.GET.get('desde', '') +" 00:00:00")
        lecturas_serializer = LecturaSerializer(lecturas, many=True)
        return Response(lecturas_serializer.data)
    
    
@api_view(['POST',])
def contacto_view(request):
    if request.method == "POST":
        serializer = ContactoSerializer(data=request.data)
        if serializer.is_valid():
            nombre = serializer.validated_data.get('nombre', None)
            apellido = serializer.validated_data.get('apellido', None)
            email = serializer.validated_data.get('email', None)
            mensaje = serializer.validated_data.get('mensaje', None)
            send_mail(
                'Contacto Form mail from ' + nombre+ " " + apellido ,
                mensaje + "\n\nResponder a: " + email,
                email,
                ['cagarcia.ush@gmail.com'],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


