from django.contrib import admin
from .models import (
    ConfiguracionUsuario,
    ListaPersonal,
    Cancion,
    TiempoLiturgico,
    ListaCancion,
    Favorito,
    LineaCancion
)
from django.contrib.auth.models import User  # Usamos el modelo de usuario de Django


@admin.register(ConfiguracionUsuario)
class ConfiguracionUsuarioAdmin(admin.ModelAdmin):
    list_display = ("id_usuario", "modo_oscuro", "ultima_tonalidad")



@admin.register(ListaPersonal)
class ListaPersonalAdmin(admin.ModelAdmin):
    list_display = ("id_lista", "usuario", "nombre_lista")
    search_fields = ("nombre_lista",)


@admin.register(Cancion)
class CancionAdmin(admin.ModelAdmin):
    list_display = ("id_cancion", "titulo", "nombre_tiempo")
    search_fields = ("titulo",)

    def nombre_tiempo(self, obj):
        return obj.id_tiempo.nombre_tiempo if obj.id_tiempo else "-"
    nombre_tiempo.admin_order_field = 'id_tiempo'
    nombre_tiempo.short_description = 'Tiempo Litúrgico'


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
    list_display = ("id_linea", "linea_num", "tipo_linea", "contenido", "cancion_id")
    list_filter = ("tipo_linea",)
