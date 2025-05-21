from django.core.management.base import BaseCommand
from canciones.models import TiempoLiturgico, Cancion
import unicodedata

def limpiar_texto(texto):
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    texto_normalizado = texto_normalizado.encode('ASCII', 'ignore').decode('ASCII')
    return texto_normalizado.strip().title()

class Command(BaseCommand):
    help = 'Unifica tiempos litúrgicos duplicados'

    def handle(self, *args, **kwargs):
        normalizados = {}

        for tiempo in TiempoLiturgico.objects.all():
            nombre_normalizado = limpiar_texto(tiempo.nombre_tiempo)

            if nombre_normalizado not in normalizados:
                normalizados[nombre_normalizado] = []
            normalizados[nombre_normalizado].append(tiempo)

        for nombre_normalizado, tiempos in normalizados.items():
            if len(tiempos) > 1:
                tiempo_principal = tiempos[0]
                self.stdout.write(f"Unificando duplicados de: {nombre_normalizado}")

                for duplicado in tiempos[1:]:
                    Cancion.objects.filter(id_tiempo=duplicado.id_tiempo).update(id_tiempo=tiempo_principal.id_tiempo)
                    self.stdout.write(f"  Eliminando duplicado: {duplicado.id_tiempo} ({duplicado.nombre_tiempo})")
                    duplicado.delete()

        self.stdout.write(self.style.SUCCESS("✅ Tiempos litúrgicos unificados correctamente."))
