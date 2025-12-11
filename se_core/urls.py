from django.urls import path

from se_core.vistas.navegacion.principal import index, acercade, misionvision, contactanos, iniciosesion, loginn

urlpatterns = [
    path('index/', index, name='index'),
    path('acerca_de/', acercade, name='acercade'),
    path('mision_y_vision/', misionvision, name='misionvision'),
    path('contactanos/', contactanos, name='contactanos'),
    path('inicio_de_sesion/', iniciosesion, name='iniciosesion'),
    path('login/', loginn, name='login'), 
]