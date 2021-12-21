from django.db.models import fields
from rest_framework import serializers
from AntartidaFront.models import *


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('id','nombre','latitud','longitud')

class TipoMedicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMedicion
        fields = ('nombre','unidad_de_medida','color')

class MedicionSerializer(serializers.ModelSerializer):
    tipo_medicion = TipoMedicionSerializer()
    class Meta:
        model = Medicion
        fields = ('lectura','tipo_medicion','valor')

class LecturaSerializer(serializers.ModelSerializer):
    mediciones = MedicionSerializer(source='medicion_set', many=True)
    class Meta:
        model = Lectura
        fields = ('sensor_id','fecha_lectura','mediciones')

    
class SensorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('id', 'nombreSensor', 'latitud', 'longitud')
        
class SensorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('nombreSensor', 'latitud', 'longitud', 'deleted')

class SensorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('id', 'nombre', 'latitud', 'longitud') 
        
class SensorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('nombreSensor', 'latitud', 'longitud') 

    def validate_latitud(self, value):
        if 0 == value:
            raise serializers.ValidationError("La latitud no puede ser igual 0")
        return value
    
    def validate_longitud(self, value):
        if 0 == value:
            raise serializers.ValidationError("La longitud no puede ser igual 0")
        return value

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nombre', 'apellido', 'email', 'rol')
    
    def validate_email(self, value):
        email = value
        qs = Usuario.objects.filter(email__iexact=email)
        if qs.exists():
            raise serializers.ValidationError('Este email ya existe')
        return email

class ContactoSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    apellido = serializers.CharField()
    email = serializers.EmailField()
    mensaje = serializers.CharField()


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ('__all__')
