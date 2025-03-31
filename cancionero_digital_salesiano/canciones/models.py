from django.db import models

# Create your models here.
from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

class ConfiguracionUsuario(models.Model):
    id_usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    modo_oscuro = models.BooleanField(default=False)
    ultima_tonalidad = models.CharField(max_length=100, blank=True, null=True)

class ListaPersonal(models.Model):
    id_lista = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre_lista = models.CharField(max_length=255)

class Cancion(models.Model):
    id_cancion = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    id_tiempo = models.ForeignKey('TiempoLiturgico', on_delete=models.SET_NULL, null=True, blank=True)

class TiempoLiturgico(models.Model):
    id_tiempo = models.AutoField(primary_key=True)
    nombre_tiempo = models.CharField(max_length=255)

class ListaCancion(models.Model):
    lista = models.ForeignKey(ListaPersonal, on_delete=models.CASCADE)
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)

class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)

class LineaCancion(models.Model):
    id_linea = models.AutoField(primary_key=True)
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)
    linea_num = models.IntegerField()
    tipo_linea = models.CharField(max_length=50)
    contenido = models.TextField()
