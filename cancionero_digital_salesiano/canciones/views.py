from django.shortcuts import render, get_object_or_404
from .models import Cancion, TiempoLiturgico
from datetime import date

def index(request):
    tiempo_actual = TiempoLiturgico.objects.first()  # Aquí deberías determinar el tiempo litúrgico actual con lógica real
    canciones = Cancion.objects.filter(id_tiempo=tiempo_actual)
    return render(request, 'canciones/index.html', {
        'tiempo_actual': tiempo_actual,
        'canciones': canciones,
    })

def song_detail(request, pk):
    cancion = get_object_or_404(Cancion, pk=pk)
    return render(request, 'canciones/song_detail.html', {'cancion': cancion})

def buscar_cancion(request):
    query = request.GET.get('q')
    canciones = Cancion.objects.filter(titulo__icontains=query) if query else []
    return render(request, 'canciones/busqueda.html', {
        'query': query,
        'canciones': canciones,
    })
