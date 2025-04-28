from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página de inicio con canciones por tiempo litúrgico
    path('cancion/<int:pk>/', views.song_detail, name='detalle_cancion'),  # Detalle de canción
    #path('buscar/', views.buscar_cancion, name='buscar_cancion'),  # Búsqueda de canciones
    path('search/', views.search, name='search'),

]
