"""
URL configuration for cancionero_digital_salesiano project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from canciones import views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Ruta al panel de administración de Django
    path('admin/', admin.site.urls),

    # Raíz del sitio  ➜  reenvía a las URLs de la app “canciones”
    #    - «include('canciones.urls')» carga cancionero_digital_salesiano/canciones/urls.py
    path('', include('canciones.urls')),

    # Todas las rutas que empiecen por /accounts/ las gestiona django-allauth
    path('accounts/', include('allauth.urls')),

    path('toggle-lista/', views.toggle_list, name='toggle_list'),

    path('guardar-en-lista/<int:cancion_id>/', views.guardar_cancion_en_lista, name='guardar_cancion_en_lista'),

]