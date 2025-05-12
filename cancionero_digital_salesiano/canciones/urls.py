from django.urls import path
from . import views

urlpatterns = [
    #Página de inicio
    path('', views.index, name='index'),  # Página de inicio con canciones por tiempo litúrgico
    #Página de detalles de la canción
    path('cancion/<int:pk>/', views.song_detail, name='detalle_cancion'),  # Detalle de canción
    #Pagina de canciones (Lista completa de canciones)
    path('canciones/', views.canciones_complete, name='canciones'),  # Lista de canciones

    path('search/', views.search, name='search'),

]
