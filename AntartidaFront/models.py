from django.db import models
from django.db.models import query


class Rol(models.Model):
    nombre_rol = models.CharField(max_length=30)
    deleted = models.BooleanField(default=False)

    def _str_(self):
        return self.nombreRol


class Sensor(models.Model):

    # esto lo que hace retornar por defecto solo los sensores que tienen deleted=false
    # en lugar de hacer Objects.all() cuando hacemos la query, hacemos SensoresObjects y devuelve solo los que no estan borrados
    class SensoresObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(deleted=False)

    # idSensor=models.AutoField(primary_key= True)
    nombre = models.CharField(max_length=30, unique=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    objects = models.Manager()  # default model manager
    sensores_objects = SensoresObjects()  # custom manager

    def _str_(self):
        return self.nombre


class TipoEvento(models.Model):
    # solo tiene nombre porque es para identificarlo si en un futuro se agregan mas eventos creables por el usuario
    nombre = models.CharField(max_length=30)
    deleted = models.BooleanField(default=False)

    def _str_(self):
        return self.nombre


class TipoMedicion(models.Model):

    class TipoMedicionesObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(deleted=False)

    # idTipoMedicion=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    unidad_de_medida = models.CharField(max_length=30, null=True, blank=True)
    color = models.CharField(max_length=50, default='rgba(255, 99, 132, 0.5)', null=True, blank=True)
    deleted = models.BooleanField(default=False)
    tipo_mediciones_objects = TipoMedicionesObjects()

    def _str_(self):
        return self.nombre + 'unidad:' + self.unidad_de_medida


class Usuario(models.Model):

    class UsuariosObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(deleted=False)

    class UsuariosEditores(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(rol=1)  # editor

    # idUsuario=models.AutoField(primary_key= True)
    nombre = models.CharField(max_length=30)
    password = models.CharField(max_length=150, null=False, blank=False)
    apellido = models.CharField(max_length=30)
    email = models.CharField(max_length=50, unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    deleted = models.BooleanField(default=False)
    objects = models.Manager()  # default model manager
    usuarios_editores = UsuariosEditores()  # editores
    usuarios_objects = UsuariosObjects()  # custom manager

    def _str_(self):
        return self.nombre + self.apellido + 'email: ' + self.email


class Evento(models.Model):

    class EventosObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(deleted=False)

    titulo_evento = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=300)
    usuario = models.ForeignKey(
        Usuario, null=True, blank=True, on_delete=models.CASCADE)
    sensor = models.ForeignKey(
        Sensor, null=True, blank=True, on_delete=models.CASCADE)
    fecha_evento = models.DateTimeField(auto_now_add=False)
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    objects = models.Manager()  # default model manager
    eventos_objects = EventosObjects()  # custom manager

    def _str_(self):
        return self.tituloEvento

    class Meta:
        ordering = ('-fecha_evento',)


class Lectura(models.Model):

    class LecturasObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(deleted=False)

    # idLectura=models.AutoField(primary_key=True)
    # esta es la clave foranea al sensor
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    fecha_lectura = models.DateTimeField(auto_now_add=False)
    # este campo es por si quiere agregarle alguna informacion relacionada a la lectura (por ej. midio 200 grados porque....)
    info_adicional = models.CharField(max_length=300, null=True)
    deleted = models.BooleanField(default=False)
    objects = models.Manager()  # default model manager
    lecturas_objects = LecturasObjects()  # custom manager

    def str(self):
        return self.sensor.nombre + self.fecha_lectura

    class Meta:
        ordering = ('-fecha_lectura',)


class Medicion(models.Model):

    class MedicionesObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(deleted=False)

    # idMedicion=models.AutoField(primary_key=True)
    # esta es la clave foranea al sensor
    lectura = models.ForeignKey(Lectura, on_delete=models.CASCADE)
    # esta es la clave foranea a la lectura
    tipo_medicion = models.ForeignKey(TipoMedicion, on_delete=models.PROTECT)
    # on_delete=models.CASCADE
    # tiene un largo de 300 caracteres porque si es una imagen le vamos a pasar el path
    valor = models.CharField(max_length=300)
    deleted = models.BooleanField(default=False)
    objects = models.Manager()  # default model manager
    mediciones_objects = MedicionesObjects()  # custom manager

    def _str_(self):
        return self.tipo_medicion + self.valor
