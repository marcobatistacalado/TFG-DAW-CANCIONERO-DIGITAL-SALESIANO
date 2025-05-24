from django.urls import path
from . import views

urlpatterns = [
    # Página de inicio – muestra canciones del tiempo litúrgico
    path('', views.index, name='index'),

    # Detalle de una canción concreta  (http://…/cancion/23/)
    path('cancion/<int:pk>/', views.song_detail, name='detalle_cancion'),

    # Lista completa de canciones  (http://…/canciones/)
    path('canciones/', views.canciones_complete, name='canciones'),

    # Buscador  (http://…/search/?q=…)
    path('search/', views.search, name='search'),
]
