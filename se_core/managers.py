from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UsuarioManager(BaseUserManager):
    """
     Clase para la perzonalización de usuarios donde el correo es el campo único identificador para la autenticación de un usuario en lugar del nombre de usuario en el aplicativo Django.
    """
    def create_user(self, correo, password=None, **extra_fields):
        """
        funcion para crear y guardar un usuario con el correo y la contraseña.
        
        :param self: Referencia al propio objeto.
        :param correo: Correo electrónico del usuario.
        :param password: Contraseña del usuario.
        :param extra_fields: Campos adicionales para el usuario.
        """
        if not correo:
            raise ValueError(_('El correo electrónico es obligatorio'))
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        """
        Función para crear y guardar un superusuario con el correo y la contraseña.
        
        :param self: Referencia al propio objeto.
        :param correo: Correo electrónico del superusuario.
        :param password: Contraseña del superusuario.
        :param extra_fields: Campos adicionales para el superusuario.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('El superusuario debe tener el campo is_staff=True'))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('El superusuario debe tener el campo is_superuser=True'))
        
        return self.create_user(correo, password, **extra_fields)
    