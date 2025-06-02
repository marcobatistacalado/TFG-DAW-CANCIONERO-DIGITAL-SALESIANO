from django.urls import path
from . import views
from .views import profile

urlpatterns = [
    # Página de inicio – muestra canciones del tiempo litúrgico
    path('', views.index, name='index'),

    # Detalle de una canción concreta  (http://…/cancion/23/)
    path('cancion/<int:id_cancion>/', views.detalle_cancion, name='detalle_cancion'),

    # Lista completa de canciones  (http://…/canciones/)
    path('canciones/', views.canciones_complete, name='canciones'),

    # Buscador  (http://…/search/?q=…)
    path('search/', views.search, name='search'),

    path('profile/', profile, name='account_profile'),


    path('privacidad/', views.politica_privacidad, name='privacidad'),
    path('aviso-legal/', views.aviso_legal, name='aviso_legal'),
    path('cookies/', views.politica_cookies, name='cookies'),
    path('terminos/', views.terminos_condiciones, name='terminos'),
    path('toggle_favorito/', views.toggle_favorito, name='toggle_favorito'),
    path('favoritos/', views.favoritos, name='favoritos'),

    path('lista/', views.lista, name='lista'),

    path('lista/<int:id_lista>/', views.lista_detalle, name='lista_detalle'),

    path('listas/<int:id_lista>/exportar-word/', views.exportar_lista_word, name='exportar_lista_word'),
]
