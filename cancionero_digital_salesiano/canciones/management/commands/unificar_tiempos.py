from django.core.management.base import BaseCommand
from canciones.models import TiempoLiturgico, Cancion
import unicodedata

def limpiar_texto(texto):
    """
    Normaliza y limpia un texto:
    - Elimina acentos y caracteres especiales usando Unicode NFKD.
    - Convierte a ASCII ignorando caracteres no ASCII.
    - Elimina espacios al inicio y final.
    - Capitaliza la primera letra de cada palabra.
    Retorna el texto limpio listo para comparación.
    """
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    texto_normalizado = texto_normalizado.encode('ASCII', 'ignore').decode('ASCII')
    return texto_normalizado.strip().title()

class Command(BaseCommand):
    help = 'Unifica tiempos litúrgicos duplicados'

    def handle(self, *args, **kwargs):
        # Diccionario para agrupar tiempos litúrgicos normalizados
        normalizados = {}

        # Recorremos todos los tiempos litúrgicos para agrupar por nombre normalizado
        for tiempo in TiempoLiturgico.objects.all():
            nombre_normalizado = limpiar_texto(tiempo.nombre_tiempo)

            if nombre_normalizado not in normalizados:
                normalizados[nombre_normalizado] = []
            normalizados[nombre_normalizado].append(tiempo)

        # Para cada grupo con nombres duplicados, unificamos las referencias y borramos duplicados
        for nombre_normalizado, tiempos in normalizados.items():
            if len(tiempos) > 1:
                tiempo_principal = tiempos[0]  # Tomamos el primer registro como principal
                self.stdout.write(f"Unificando duplicados de: {nombre_normalizado}")

                for duplicado in tiempos[1:]:
                    # Actualizamos las canciones que apuntaban al duplicado para que apunten al principal
                    Cancion.objects.filter(id_tiempo=duplicado.id_tiempo).update(id_tiempo=tiempo_principal.id_tiempo)
                    self.stdout.write(f"  Eliminando duplicado: {duplicado.id_tiempo} ({duplicado.nombre_tiempo})")
                    # Borramos el registro duplicado del tiempo litúrgico
                    duplicado.delete()

        # Mensaje final indicando éxito
        self.stdout.write(self.style.SUCCESS("✅ Tiempos litúrgicos unificados correctamente."))
