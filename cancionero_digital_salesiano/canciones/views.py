from django.shortcuts import render, get_object_or_404
from datetime import date, timedelta
from .models import Cancion, TiempoLiturgico
from django.template.loader import render_to_string
from django.http import JsonResponse
import re
from django.contrib.auth.decorators import login_required

# ============================
# 🗓 CÁLCULOS DE FECHAS Y TIEMPOS LITÚRGICOS
# ============================

def calcular_fecha_pascua(anio):
    """
    Calcula la fecha de Pascua para un año dado según el algoritmo Computus.
    Retorna un objeto date con la fecha exacta de Pascua para ese año.
    """
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

def obtener_tiempo_liturgico_actual():
    """
    Devuelve el nombre del tiempo litúrgico actual basado en la fecha actual.
    Calcula los rangos de fechas para Adviento, Navidad, Cuaresma, Pascua, y Tiempo Ordinario.
    Retorna el nombre del tiempo litúrgico activo o 'Ampliación' si no coincide con ninguno.
    """
    hoy = date.today()
    anio = hoy.year

    # Calculamos fechas clave usando la fecha de Pascua
    pascua = calcular_fecha_pascua(anio)
    cuaresma_inicio = pascua - timedelta(days=46)
    cuaresma_fin = pascua - timedelta(days=1)
    pascua_fin = pascua + timedelta(days=49)  # Hasta Pentecostés

    navidad_inicio = date(anio, 12, 25)
    bautismo_senor = navidad_inicio + timedelta(days=19)
    tiempo_ordinario_1 = bautismo_senor + timedelta(days=1)
    tiempo_ordinario_2 = pascua_fin + timedelta(days=1)

    # Calculo del cuarto domingo antes de Navidad (inicio de Adviento)
    cuarto_domingo_antes_navidad = navidad_inicio - timedelta(days=((navidad_inicio.weekday() + 1) % 7) + 21)
    adviento_inicio = cuarto_domingo_antes_navidad
    cristo_rey = adviento_inicio - timedelta(days=7)

    # Determinamos en qué periodo litúrgico estamos
    if adviento_inicio <= hoy < navidad_inicio:
        return 'Adviento'
    elif navidad_inicio <= hoy <= bautismo_senor:
        return 'Navidad'
    elif cuaresma_inicio <= hoy <= cuaresma_fin:
        return 'Cuaresma'
    elif pascua <= hoy <= pascua_fin:
        return 'Pascua'
    elif tiempo_ordinario_1 <= hoy < cuaresma_inicio:
        return 'Tiempo Ordinario'
    elif tiempo_ordinario_2 <= hoy < adviento_inicio:
        return 'Tiempo Ordinario'
    else:
        return 'Ampliación'  # Valor por defecto si no coincide con los anteriores

def obtener_tiempo_liturgico(id_tiempo):
    """
    Recupera el objeto TiempoLiturgico por su id.
    Si no existe, lanza error 404.
    """
    return get_object_or_404(TiempoLiturgico, id_tiempo=id_tiempo)

# ============================
# 🏠 VISTAS PRINCIPALES DE LA APLICACIÓN
# ============================

def index(request):
    """
    Vista principal que muestra las canciones correspondientes al tiempo litúrgico actual.
    Si no se encuentra, muestra las canciones del tiempo 'Ampliación' por defecto.
    """
    nombre_tiempo = obtener_tiempo_liturgico_actual()
    tiempo_actual = TiempoLiturgico.objects.filter(nombre_tiempo__iexact=nombre_tiempo).first()

    if not tiempo_actual:
        # Si no se encuentra el tiempo litúrgico calculado, usa 'Ampliación'
        tiempo_actual = TiempoLiturgico.objects.filter(nombre_tiempo__iexact="Ampliación").first()

    # Obtener canciones filtradas por el tiempo litúrgico actual
    canciones = Cancion.objects.filter(id_tiempo=tiempo_actual.id_tiempo) if tiempo_actual else Cancion.objects.none()

    return render(request, 'canciones/index.html', {
        'tiempo_actual': tiempo_actual,
        'canciones': canciones,
    })

def canciones_complete(request):
    tiempos = TiempoLiturgico.objects.all()  # Todos los tiempos litúrgicos disponibles

    canciones_por_tiempo = {}  # Diccionario para almacenar canciones agrupadas

    for tiempo in tiempos:
        canciones_por_tiempo[tiempo.nombre_tiempo] = Cancion.objects.filter(id_tiempo=tiempo.id_tiempo)



    return render(request, 'canciones/toggleCanciones.html', {
        'canciones_por_tiempo': canciones_por_tiempo,
        'tiempos': tiempos,
    })

# ============================
# 🎸 FUNCIONES DE TRANSPOSE DE ACORDES
# ============================

# Lista de notas musicales en español con sostenidos (#)
NOTAS_ESP = ["DO", "DO#", "RE", "RE#", "MI", "FA", "FA#", "SOL", "SOL#", "LA", "LA#", "SI"]

# Diccionario para normalizar acordes alterados o con nomenclaturas especiales
NORMALIZAR = {
    "E#": "FA", "B#": "DO",
    "FB": "MI", "CB": "SI",
    "FA##": "SOL", "DO##": "RE",
    "MI#": "FA", "SI#": "DO",
}

def obtener_base_y_sufijo(acorde):
    """
    Separa la base del acorde (ejemplo: DO#) y el sufijo (ejemplo: m7).
    Convierte a mayúsculas para hacer la búsqueda.
    Retorna una tupla (base, sufijo).
    """
    acorde_original = acorde.strip().replace("♯", "#")  # Normaliza sostenidos
    acorde_mayus = acorde_original.upper()

    # Buscamos qué base musical coincide al inicio del acorde
    for base in sorted(NOTAS_ESP, key=len, reverse=True):
        if acorde_mayus.startswith(base):
            sufijo = acorde_original[len(base):]  # Lo que sobra después de la base es sufijo
            return base, sufijo
    return None, None  # Si no se encuentra base

def transponer_acorde(acorde, semitonos):
    """
    Transpone un acorde dada una cantidad de semitonos.
    Busca la base, la mueve en la lista NOTAS_ESP, y devuelve el nuevo acorde con sufijo.
    """
    base, sufijo = obtener_base_y_sufijo(acorde)
    if base not in NOTAS_ESP:
        # Si no reconoce la base, devuelve el acorde tal cual (no transpone)
        return acorde
    idx = NOTAS_ESP.index(base)
    nuevo_idx = (idx + semitonos) % len(NOTAS_ESP)
    nuevo_base = NOTAS_ESP[nuevo_idx]

    # Normaliza si el acorde resultante está en el diccionario NORMALIZAR
    if nuevo_base + sufijo in NORMALIZAR:
        return NORMALIZAR[nuevo_base + sufijo]

    return nuevo_base + sufijo

def transponer_linea(linea, semitonos=1):
    """
    Busca todos los acordes en una línea de texto y los transpone la cantidad de semitonos indicada.
    Usa expresiones regulares para identificar acordes.
    """
    pattern = r'\b([A-ZÑa-zñ]{2,4}#?(m7|maj7|7M|m|7|sus4|sus2|6|m6)?)\b'

    def reemplazo(match):
        acorde = match.group(0)
        return transponer_acorde(acorde, semitonos)

    # Reemplaza cada acorde encontrado por su versión transpuesta
    return re.sub(pattern, reemplazo, linea)

# ============================
# 🎵 VISTA DETALLE DE CANCIÓN CON TRANSPOSE
# ============================

def song_detail(request, pk):
    """
    Vista detalle de una canción que permite transponer acordes.
    Recibe el parámetro 'transpose' por GET para modificar el tono.
    Si la petición es AJAX, devuelve solo el fragmento HTML con las líneas transpuestas.
    """
    cancion = get_object_or_404(Cancion, pk=pk)
    lineas = cancion.lineacancion_set.all().order_by('linea_num')
    semitonos = int(request.GET.get('transpose', 0))

    lineas_transpuestas = []
    for linea in lineas:
        contenido = linea.contenido
        # Solo transpone las líneas que son acordes y si semitonos != 0
        if linea.tipo_linea == 'acorde' and semitonos != 0:
            contenido = transponer_linea(contenido, semitonos)
        lineas_transpuestas.append({
            'contenido': contenido,
            'tipo_linea': linea.tipo_linea
        })

    # Si es una petición AJAX, devolver solo fragmento para actualización dinámica
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('canciones/lineas_fragment.html', {'lineas': lineas_transpuestas})
        return JsonResponse({'html': html})

    # Render normal de la página completa
    return render(request, 'canciones/cancion.html', {
        'cancion': cancion,
        'lineas': lineas_transpuestas,
        'semitonos': semitonos,
    })

# ============================
# 🔍 FUNCIONALIDAD DE BÚSQUEDA
# ============================

def search(request):
    """
    Busca canciones por título que contengan la cadena 'q' enviada por GET.
    Solo realiza búsqueda si la longitud de la consulta es >= 3.
    Si es petición AJAX, devuelve fragmento HTML con resultados.
    """
    query = request.GET.get('q', '')
    nombre_tiempo = obtener_tiempo_liturgico_actual()
    tiempo_actual = TiempoLiturgico.objects.filter(nombre_tiempo__iexact=nombre_tiempo).first()

    if len(query) >= 3:
        canciones = Cancion.objects.filter(titulo__icontains=query)
    else:
        # Si la búsqueda es muy corta, muestra canciones del tiempo actual
        canciones = Cancion.objects.filter(id_tiempo=tiempo_actual.id_tiempo) if tiempo_actual else Cancion.objects.none()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('canciones/canciones_list.html', {'canciones': canciones})
        return JsonResponse({'html': html})

    return render(request, 'canciones/index.html', {
        'tiempo_actual': tiempo_actual,
        'canciones': canciones,
        'busqueda': query,
    })


@login_required
def profile(request):
    return render(request, 'account/profile.html')