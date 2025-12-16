from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission, User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import UsuarioManager

# Create your models here.
# -------------------------------- TABLAS PARAMÉTRICAS ----------------------------------
class Roles(models.Model):
    nombre_rol = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
    
    def __str__(self):
        return self.nombre


class Tipos_Documento(models.Model):
    nombre = models.CharField(max_length=60)
    
    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documentos"
    
    def __str__(self):
        return self.nombre
    
    
class Paises(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo_iso = models.CharField(max_length=3, unique=True)
    
    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
    
    def __str__(self):
        return self.nombre
    
    
class Departamentos(models.Model):
    pais = models.ForeignKey(Paises, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        
    def __str__(self):
        return self.nombre
    
    
class Ciudades(models.Model):
    nombre = models.CharField(max_length=50)
    departamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        
    def __str__(self):
        return f"{self.nombre} ({self.departamento.nombre})"
    
    
class Generos(models.Model):
    nombre = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"
    
    def __str__(self):
        return self.nombre
    
    
class Estados_Civiles(models.Model):
    nombre = models.CharField(max_length=30)
    
    class Meta:
        verbose_name = "Estado Civil"
        verbose_name_plural = "Estados Civiles"
    
    def __str__(self):
        return self.nombre
    
    
class Estratos(models.Model):
    nombre = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = "Estrato"
        verbose_name_plural = "Estratos"
    
    def __str__(self):
        return self.nombre
# ---------------------------------------------------------------------------------------
# ------------------------------- ESTRUCTURA ACADEMICA ----------------------------------

class Niveles_Educativos(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name = "Nivel Educativo"
        verbose_name_plural = "Niveles Educativos"
    
    def __str__(self):
        return self.nombre
    

class Aulas(models.Model):
    ESTADOS = [
        ('Disponible', 'Disponible'),
        ('Ocupada', 'Ocupada'),
        ('Mantenimiento', 'Mantenimiento'),
    ]
    
    nombre = models.CharField(max_length=50)
    capacidad = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Disponible')
    
    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"
        
    def __str__(self):
        return self.nombre


class Grados(models.Model):
    nivel = models.ForeignKey(Niveles_Educativos, on_delete=models.CASCADE, related_name='grados')
    nombre = models.CharField(max_length=10)
    
    class Meta:
        unique_together = ('nivel', 'nombre')
        verbose_name = "Grado"
        verbose_name_plural = "Grados"
    
    def __str__(self):
        return f"{self.nivel.nombre} - {self.nombre}"
    
    
class Areas(models.Model):
    nombre = models.CharField(max_length=100)
    obligatoria = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Área"
        verbose_name_plural = "Áreas"
    
    def __str__(self):
        return self.nombre
    

class Asignaturas(models.Model):
    nombre = models.CharField(max_length=100)
    grado = models.ForeignKey(Grados, on_delete=models.CASCADE, related_name='asignaturas')
    area = models.ForeignKey(Areas, on_delete=models.CASCADE, related_name='asignaturas')
    
    class Meta:
        unique_together = ('nombre', 'grado', 'area')
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"
        
    def __str__(self):
        return self.nombre
    
    
class Grupos(models.Model):
    grado = models.ForeignKey(Grados, on_delete=models.CASCADE, related_name='grupos')
    nombre = models.CharField(max_length=10)
    aula = models.ForeignKey(Aulas, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"
        
    def __str__(self):
        return f"{self.nombre} ({self.grado})"
    
    
class Temas(models.Model):
    asignatura = models.ForeignKey(Asignaturas, on_delete=models.CASCADE, related_name='temas')
    nombre = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbosa_name = "Tema"
        verbose_name_plural = "Temas"
        
    def __str__(self):
        return f"{self.nombre} - {self.asignatura.nombre}"
    
# ---------------------------------------------------------------------------------------
# ---------------------------------- USUARIOS -------------------------------------------
class Usuarios(AbstractBaseUser, PermissionsMixin):
    correo = models.EmailField(_('Dirección de correo electrónico'), unique=True)
    rol = models.ForeignKey(Roles, on_delete=models.PROTECT, null=True, blank=True)
    
   # tipo_documento = models.ForeignKey(Tipos_Documento, on_delete=models.PROTECT, null=True)
   # numero_documento = models.CharField(max_length=20, unique=True, null=True)
    
   # municipio_identificacion = models.ForeignKey(
   #     Ciudades,
   #     null=True,
   #     blank=True,
   #     on_delete=models.SET_NULL,
   #     related_name='usuarios_municipio_identificacion'
   # )
    
    activado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='Usuarios_activados',
        verbose_name='Activado por'
    )
    
    fecha_creacion = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(Group, blank=True, related_name='usuario_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='usuario_set')
    
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = []
    
    objects = UsuarioManager()
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        
    def __str__(self):
        return self.correo