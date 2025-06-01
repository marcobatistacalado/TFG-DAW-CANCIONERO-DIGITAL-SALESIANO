from django.db import models
from django.contrib.auth.models import User


class ConfiguracionUsuario(models.Model):
    id_usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Usuario',
        help_text='Usuario al que pertenece esta configuración'
    )
    modo_oscuro = models.BooleanField(
        default=False,
        verbose_name='Modo oscuro',
        help_text='Indica si el usuario prefiere el modo oscuro'
    )
    ultima_tonalidad = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Última tonalidad utilizada'
    )

    def __str__(self):
        return f"Configuración de {self.id_usuario.username}"


class ListaPersonal(models.Model):
    id_lista = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuario'
    )
    nombre_lista = models.CharField(
        max_length=255,
        verbose_name='Nombre de la lista'
    )

    def __str__(self):
        return f"{self.nombre_lista} ({self.usuario.username})"


class TiempoLiturgico(models.Model):
    id_tiempo = models.AutoField(primary_key=True)
    nombre_tiempo = models.CharField(
        max_length=255,
        verbose_name='Nombre del tiempo litúrgico'
    )

    def __str__(self):
        return self.nombre_tiempo


class Cancion(models.Model):
    id_cancion = models.AutoField(primary_key=True)
    titulo = models.CharField(
        max_length=255,
        verbose_name='Título'
    )
    id_tiempo = models.ForeignKey(
        TiempoLiturgico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Tiempo litúrgico',
        help_text='Selecciona el tiempo litúrgico relacionado (opcional)'
    )

    def __str__(self):
        return self.titulo


class ListaCancion(models.Model):
    lista = models.ForeignKey(
        ListaPersonal,
        on_delete=models.CASCADE,
        verbose_name='Lista'
    )
    cancion = models.ForeignKey(
        Cancion,
        on_delete=models.CASCADE,
        verbose_name='Canción'
    )

    def __str__(self):
        return f"{self.cancion.titulo} en {self.lista.nombre_lista}"


class Favorito(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuario'
    )
    cancion = models.ForeignKey(
        Cancion,
        on_delete=models.CASCADE,
        verbose_name='Canción'
    )

    def __str__(self):
        return f"{self.cancion.titulo} favorito de {self.usuario.username}"


class LineaCancion(models.Model):
    id_linea = models.AutoField(primary_key=True)
    cancion = models.ForeignKey(
        Cancion,
        on_delete=models.CASCADE,
        verbose_name='Canción'
    )
    linea_num = models.IntegerField(
        verbose_name='Número de línea',
        help_text='Orden de la línea en la canción'
    )

    TIPO_LINEA_CHOICES = [
        ('acorde', 'Acorde'),
        ('normal', 'Normal'),
        ('estribillo', 'Estribillo'),
    ]
    tipo_linea = models.CharField(
        max_length=10,
        choices=TIPO_LINEA_CHOICES,
        default='normal',
        help_text='Tipo de línea: acorde, normal o estribillo',
        verbose_name='Tipo de línea'
    )
    
    contenido = models.TextField(
        verbose_name='Contenido de la línea'
    )

    def __str__(self):
        return f"{self.get_tipo_linea_display()} - Línea {self.linea_num} de {self.cancion.titulo}"
