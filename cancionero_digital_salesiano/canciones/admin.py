from django.contrib import admin
from .models import TiempoLiturgico, Cancion, LineaCancion, Favorito, ListaPersonal, ListaCancion

# ============================
# ⚙️ CONFIGURACIÓN DEL ADMINISTRADOR
# ============================


# ----------------------------
# 🎵 Canción y líneas asociadas
# ----------------------------

class LineaCancionInline(admin.TabularInline):
    """
    Permite editar las líneas de una canción directamente desde la página de administración de la canción.
    Se muestra como un formulario en línea (TabularInline).
    """
    model = LineaCancion
    extra = 1  # Número de formularios en blanco adicionales


@admin.register(Cancion)
class CancionAdmin(admin.ModelAdmin):
    """
    Configura la interfaz de administración para el modelo Cancion.
    Incluye las líneas de canción como formularios en línea.
    """
    inlines = [LineaCancionInline]
    list_display = ('titulo', 'id_tiempo')  # tuple con campos válidos
    search_fields = ['titulo']  # lista aunque sea un solo campo


# ----------------------------
# ⛪ Tiempos Litúrgicos
# ----------------------------

@admin.register(TiempoLiturgico)
class TiempoLiturgicoAdmin(admin.ModelAdmin):
    """
    Administra los objetos de Tiempo Litúrgico desde el panel de administración.
    Permite búsquedas por nombre.
    """
    list_display = ['nombre_tiempo']  # lista para un solo campo
    search_fields = ['nombre_tiempo']  # lista para un solo campo


# ----------------------------
# ⭐ Favoritos
# ----------------------------

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    """
    Gestión de favoritos en el panel de administración.
    Muestra el usuario y la canción asociada.
    """
    list_display = ('usuario', 'cancion')
    search_fields = ('usuario__username', 'cancion__titulo')


# ----------------------------
# 📜 Listas personales de usuarios
# ----------------------------

@admin.register(ListaPersonal)
class ListaPersonalAdmin(admin.ModelAdmin):
    """
    Permite la administración de listas personales creadas por los usuarios.
    Se puede buscar por nombre de lista o usuario.
    """
    list_display = ('nombre_lista', 'usuario')
    search_fields = ('nombre_lista', 'usuario__username')


# ----------------------------
# 🔗 Asociación entre canciones y listas
# ----------------------------

@admin.register(ListaCancion)
class ListaCancionAdmin(admin.ModelAdmin):
    """
    Administra las relaciones entre canciones y listas en el panel de administración.
    Útil para ver qué canciones pertenecen a qué listas.
    """
    list_display = ('lista', 'cancion')
    search_fields = ('lista__nombre_lista', 'cancion__titulo')
