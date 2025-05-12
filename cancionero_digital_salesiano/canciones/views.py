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


import re

# Lista de acordes básicos en notación latina. Se utilizará para identificar y transponer acordes.
NOTAS_ESP = ["DO", "DO#", "RE", "RE#", "MI", "FA", "FA#", "SOL", "SOL#", "LA", "LA#", "SI"]

# Diccionario para normalizar acordes inusuales o mal escritos.
NORMALIZAR = {
    "E#": "FA", "B#": "DO",        # E# y B# son notas teóricas, pero equivalen a FA y DO
    "FB": "MI", "CB": "SI",        # FB (FA bemol) = MI, CB = SI
    "FA##": "SOL", "DO##": "RE",   # Notas con doble sostenido se simplifican
    "MI#": "FA", "SI#": "DO",      # Otros casos poco comunes
}

# Esta función toma un acorde y separa su "base" (ej: DO) y su "sufijo" (ej: m7)
def obtener_base_y_sufijo(acorde):
    acorde_original = acorde.strip().replace("♯", "#")  # Reemplazamos el símbolo Unicode ♯ por #
    acorde_mayus = acorde_original.upper()              # Convertimos a mayúsculas para comparación

    # Recorremos la lista de acordes buscando el que coincida al inicio
    for base in sorted(NOTAS_ESP, key=len, reverse=True):  # Se ordena por largo para que DO# se detecte antes que DO
        if acorde_mayus.startswith(base):
            sufijo = acorde_original[len(base):]  # Se extrae el sufijo (manteniendo su formato original)
            return base, sufijo
    return None, None  # Si no se encuentra base válida

# Transpone un acorde una cantidad determinada de semitonos hacia arriba o abajo
def transponer_acorde(acorde, semitonos):
    base, sufijo = obtener_base_y_sufijo(acorde)
    
    # Si el acorde no se reconoce como válido, se devuelve tal cual
    if base not in NOTAS_ESP:
        print(f"El acorde {acorde} no se reconoce (base: {base})")
        return acorde

    idx = NOTAS_ESP.index(base)                        # Buscamos la posición actual en la escala
    nuevo_idx = (idx + semitonos) % len(NOTAS_ESP)     # Calculamos la nueva posición (circular en escala)
    nuevo_base = NOTAS_ESP[nuevo_idx]                  # Obtenemos la nueva nota base

    # Verificamos si el nuevo acorde completo requiere normalización
    if nuevo_base + sufijo in NORMALIZAR:
        return NORMALIZAR[nuevo_base + sufijo]

    return nuevo_base + sufijo  # Devolvemos acorde transpuesto

# Transpone todos los acordes encontrados en una línea de texto
def transponer_linea(linea, semitonos=1):
    # Expresión regular para detectar acordes con posibles sufijos (como m, m7, sus4, etc.)
    pattern = r'\b([A-ZÑa-zñ]{2,4}#?(m7|maj7|7M|m|7|sus4|sus2|6|m6)?)\b'

    # Reemplaza cada acorde detectado por su versión transpuesta
    def reemplazo(match):
        acorde = match.group(0)
        return transponer_acorde(acorde, semitonos)

    return re.sub(pattern, reemplazo, linea)  # Aplica la transposición en la línea completa

from django.template.loader import render_to_string

def song_detail(request, pk):
    # Obtenemos la canción específica por su clave primaria (pk).
    # Si no existe, lanzamos un error 404.
    cancion = get_object_or_404(Cancion, pk=pk)

    # Obtenemos todas las líneas asociadas a la canción, ordenadas por número de línea.
    lineas = cancion.lineacancion_set.all().order_by('linea_num')

    # Obtenemos el valor del parámetro 'transpose' (cantidad de semitonos a transponer).
    # Por defecto será 0 (sin transposición).
    semitonos = int(request.GET.get('transpose', 0))
    print("Semitonos recibidos:", semitonos)

    # Creamos una nueva lista donde guardaremos las líneas transpuestas
    lineas_transpuestas = []

    for linea in lineas:
        contenido = linea.contenido  # Texto original de la línea

        # Si es una línea de tipo "acorde" y se ha pedido transposición
        if linea.tipo_linea == 'acorde' and semitonos != 0:
            print(f"Transponiendo acorde: {contenido}")
            contenido = transponer_linea(contenido, semitonos)

        # Añadimos la línea transpuesta (o sin cambios) a la lista
        lineas_transpuestas.append({
            'contenido': contenido,
            'tipo_linea': linea.tipo_linea
        })

    # Si la petición viene por AJAX (desde JS), devolvemos solo el fragmento HTML necesario
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('canciones/lineas_fragment.html', {'lineas': lineas_transpuestas})
        return JsonResponse({'html': html})

    # Si no es AJAX, renderizamos la página completa del detalle de la canción
    return render(request, 'canciones/cancion.html', {
        'cancion': cancion,
        'lineas': lineas_transpuestas,
        'semitonos': semitonos  # Para mostrar el estado actual de transposición en el frontend
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