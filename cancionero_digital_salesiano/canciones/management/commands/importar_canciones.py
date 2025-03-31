import json
from django.core.management.base import BaseCommand
from canciones.models import Cancion, LineaCancion, TiempoLiturgico

class Command(BaseCommand):
    help = 'Importa canciones desde un archivo JSON'

    def handle(self, *args, **kwargs):
        with open("CazAppDB.songs.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            # Buscar o crear el tiempo litúrgico si existe
            tiempo = None
            if "section" in item and item["section"].strip():
                tiempo, _ = TiempoLiturgico.objects.get_or_create(nombre_tiempo=item["section"])

            # Crear la canción
            cancion, created = Cancion.objects.get_or_create(
                titulo=item["title"],
                defaults={"id_tiempo": tiempo}
            )

            # Agregar líneas de la canción
            for line in item["body"]:
                LineaCancion.objects.create(
                    cancion=cancion,
                    linea_num=line["line"],
                    tipo_linea=line["type"],
                    contenido=line["content"]
                )

        self.stdout.write(self.style.SUCCESS('Canciones importadas correctamente.'))
