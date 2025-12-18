from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Usuarios

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ('correo',)
        
class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuarios
        fields = ('correo',)