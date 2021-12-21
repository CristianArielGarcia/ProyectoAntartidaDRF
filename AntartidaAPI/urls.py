from django.urls import path
from .views import *

app_name = 'AntartidaAPI'

urlpatterns = [
    # URLS DE LOS SENSORES
    path('Sensor/Delete/<int:id>', sensor_delete_view, name='sensor_delete'),
    path('Sensor/Detail/<int:id>', sensor_detail_view, name='sensor_detail'),
    path('Sensor/Update/<int:id>', sensor_detail_view, name='sensor_update'),
    path('Sensor/GetAll', sensor_view, name='list'),
    path('Sensor/create', sensor_view, name='sensor_create'),
    
    # path('Sensor/detail/<int:id>/', sensor_detail_view, name='sensor_detail_view'),
    path('Sensor/<int:sensor>/Lecturas/GetAllByFecha', sensor_lecturas_por_fecha_view, name='sensor_lecturas_por_fecha_view'),

    #URL DE CONTACTO
    path('contacto/create/',contacto_view,name='contacto'),
    
    # URLS DEl ROL
    # path('rol/', RolList.as_view(), name='listCreate'),

    #URLS DE LAS LECTURA
    path('Lectura/by-sensor/<int:sensor>/', lectura_view, name='list'),
    path('lectura/detail/<int:id>/', lectura_detail_view, name='lectura_detail_view'),
    path('lectura/create', lectura_view, name='create'),
    
    #URLS DE LAS MEDICION
    path('medicion/', medicion_view, name='list'),
    path('medicion/detail/<int:id>/', medicion_detail_view, name='medicion_detail_view'),
    path('medicion/create', medicion_view, name='create'),
    
    #URLS DE LOS TIPO MEDICION
    path('TipoMedicion/', tipo_medicion_view, name='list'),
    

    # URLS DE LOS USUARIOS
    path('usuario/', usuario_view, name='list'),
    path('usuario/detail/<int:id>/', usuario_detail_view, name='usuario_detail_view'),
    path('usuario/create', usuario_view, name='create'),

]
