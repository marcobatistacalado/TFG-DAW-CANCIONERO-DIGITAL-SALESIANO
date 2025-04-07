from django.contrib import admin
from .models import (
    Usuario,
    ConfiguracionUsuario,
    ListaPersonal,
    Cancion,
    TiempoLiturgico,
    ListaCancion,
    Favorito,
    LineaCancion
)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id_usuario", "nombre", "email")
    search_fields = ("nombre", "email")

@admin.register(ConfiguracionUsuario)
class ConfiguracionUsuarioAdmin(admin.ModelAdmin):
    list_display = ("id_usuario", "modo_oscuro", "ultima_tonalidad")

@admin.register(ListaPersonal)
class ListaPersonalAdmin(admin.ModelAdmin):
    list_display = ("id_lista", "usuario", "nombre_lista")
    search_fields = ("nombre_lista",)

@admin.register(Cancion)
class CancionAdmin(admin.ModelAdmin):
    list_display = ("id_cancion", "titulo", "id_tiempo")
    search_fields = ("titulo",)

@admin.register(TiempoLiturgico)
class TiempoLiturgicoAdmin(admin.ModelAdmin):
    list_display = ("id_tiempo", "nombre_tiempo")

@admin.register(ListaCancion)
class ListaCancionAdmin(admin.ModelAdmin):
    list_display = ("lista", "cancion")

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "cancion")

@admin.register(LineaCancion)
class LineaCancionAdmin(admin.ModelAdmin):
    list_display = ("id_linea", "linea_num", "tipo_linea", "contenido", "linea_num", "cancion_id")
    list_filter = ("tipo_linea",)
