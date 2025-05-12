from django.shortcuts import render, get_object_or_404
from datetime import date, timedelta
from .models import Cancion, TiempoLiturgico
from datetime import date, timedelta
from django.template.loader import render_to_string
from django.http import JsonResponse

'''
Funcion para calcular la fecha de Pascua según el algoritmo de Computus.
En el calendario gregoriano.
'''
def calcular_fecha_pascua(anio):
    a = anio % 19
    b = anio // 100
    c = anio % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return date(anio, mes, dia)

'''
Funcion para obtener el tiempo litúrgico actual.
En caso de no esncontrar un tiempo litúrgico válido, se asigna "Ampliación" por defecto.

Duda?? El tema de los tiempor no lo tenemos cuadrado con la bbdd (revisar ese aspecto)
'''
def obtener_tiempo_liturgico_actual():
    hoy = date.today()
    anio = hoy.year

    pascua = calcular_fecha_pascua(anio)
    cuaresma_inicio = pascua - timedelta(days=46)
    cuaresma_fin = pascua - timedelta(days=1)
    pascua_fin = pascua + timedelta(days=49)  # Pentecostés

    navidad_inicio = date(anio, 12, 25)
    bautismo_senor = navidad_inicio + timedelta(days=19)
    tiempo_ordinario_1 = bautismo_senor + timedelta(days=1)
    tiempo_ordinario_2 = pascua_fin + timedelta(days=1)

    # Calcular el cuarto domingo antes de Navidad (inicio de Adviento)
    navidad = date(anio, 12, 25)
    cuarto_domingo_antes_navidad = navidad - timedelta(days=((navidad.weekday() + 1) % 7) + 21)
    adviento_inicio = cuarto_domingo_antes_navidad

    cristo_rey = adviento_inicio - timedelta(days=7)  # domingo anterior a Adviento

    # Asignar un tiempo litúrgico basado en la fecha actual
    if hoy >= adviento_inicio and hoy < navidad_inicio:
        return 'Adviento'
    elif hoy >= navidad_inicio and hoy <= bautismo_senor:
        return 'Navidad'
    elif hoy >= cuaresma_inicio and hoy <= cuaresma_fin:
        return 'Cuaresma'
    elif hoy >= pascua and hoy <= pascua_fin:
        return 'Pascua'
    elif hoy >= tiempo_ordinario_1 and hoy < cuaresma_inicio:
        return 'Tiempo Ordinario'
    elif hoy >= tiempo_ordinario_2 and hoy < adviento_inicio:
        return 'Tiempo Ordinario'
    else:
        # Si no se encuentra un tiempo litúrgico válido, asignar "Ampliacion" por defecto
        return 'Ampliación'


'''
Funcion para obtener el tiempo litúrgico por su id.
En caso de no encontrarlo, se lanza un error 404.
'''
def obtener_tiempo_liturgico(id_tiempo):
    tiempo_liturgico = get_object_or_404(TiempoLiturgico, id_tiempo=id_tiempo)
    return tiempo_liturgico


'''
Funcion para la visualicacion de la vista inicial.
Obtenemos lo siguiente:
- El tiempo litúrgico actual (si no se encuentra, se asigna "Ampliación" por defecto).
- Las canciones que pertenecen a ese tiempo litúrgico.
- Si no se encuentra un tiempo litúrgico, se asigna una lista vacía de canciones.
'''
def index(request):
    nombre_tiempo = obtener_tiempo_liturgico_actual()  # Obtener el tiempo litúrgico actual
    # Obtener el objeto TiempoLiturgico correspondiente al tiempo litúrgico actual
    tiempo_actual = TiempoLiturgico.objects.filter(nombre_tiempo__iexact=nombre_tiempo).first()

    if not tiempo_actual:
        # Si no se encuentra un tiempo litúrgico, asignar el de "Ampliación" por defecto
        tiempo_actual = TiempoLiturgico.objects.filter(nombre_tiempo__iexact="Ampliación").first() # Revisar que es lo que muestra esto, sino otra opcion seria meter las canciones de don bosco

    if tiempo_actual:
        # Filtrar las canciones por el id_tiempo
        canciones = Cancion.objects.filter(id_tiempo=tiempo_actual.id_tiempo)
    else:
        canciones = Cancion.objects.none() # Revisar que es lo que muestra esto, sino otra opcion seria meter las canciones de don bosco

    # Será el renderizado de la vista inicial con los datros obtenidos
    return render(request, 'canciones/index.html', {
        'tiempo_actual': tiempo_actual,
        'canciones': canciones,
    })


'''
Funcion para la visualizacion de la vista de detalles de la canción.
Obtenemos lo siguiente:
- La canción seleccionada por el usuario (si no se encuentra, se lanza un error 404).
- El tiempo litúrgico actual (si no se encuentra, se asigna "Ampliación" por defecto).
- Las líneas de la canción seleccionada, ordenadas por el número de línea.
'''
def song_detail(request, pk):
    cancion = get_object_or_404(Cancion, pk=pk)
    tiempo_actual = cancion.id_tiempo
    lineas = cancion.lineacancion_set.all().order_by('linea_num')  # relación inversa por ForeignKey

    return render(request, 'canciones/cancion.html', {
        'cancion': cancion,
        'tiempo_actual': tiempo_actual,
        'lineas': lineas
    })

'''
Funcion de busqueda de las canciones.
Donde recibimos la query de busqueda trabajada en el script de javascript.
Nos devolverá una lista de canciones dodne el titulo contenga la query.
'''
def search(request):
    query = request.GET.get('q', '')
    nombre_tiempo = obtener_tiempo_liturgico_actual()
    tiempo_actual = TiempoLiturgico.objects.filter(nombre_tiempo__iexact=nombre_tiempo).first()

    if len(query) >= 3:
        canciones = Cancion.objects.filter(titulo__icontains=query)
    else:
        canciones = Cancion.objects.filter(id_tiempo=tiempo_actual.id_tiempo) if tiempo_actual else Cancion.objects.none()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('canciones/canciones_list.html', {'canciones': canciones})
        return JsonResponse({'html': html})

    # Aquí renderizamos el index.html completo pero con búsqueda
    return render(request, 'canciones/index.html', {
        'tiempo_actual': tiempo_actual,
        'canciones': canciones,
        'busqueda': query  # 👈 Este valor activa el título "Buscando:"
    })

def canciones_complete(request):
    canciones = Cancion.objects.all()
    return render (request, 'canciones/index.html', {
        'canciones': canciones,
    })

def canciones_complete(request):
    canciones = Cancion.objects.all()
    return render (request, 'canciones/index.html', {
        'canciones': canciones,
    })