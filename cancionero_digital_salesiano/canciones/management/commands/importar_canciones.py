import json
from django.core.management.base import BaseCommand
from canciones.models import Cancion, LineaCancion, TiempoLiturgico

class Command(BaseCommand):
    help = 'Importa canciones desde un archivo JSON'

    def handle(self, *args, **kwargs):
        # Abrimos y cargamos el archivo JSON con las canciones
        with open("CazAppDB.songs.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # Iteramos sobre cada canción en el JSON
        for item in data:
            tiempo = None
            # Si el item tiene una sección (tiempo litúrgico), intentamos obtenerla o crearla
            if "section" in item and item["section"].strip():
                tiempo, _ = TiempoLiturgico.objects.get_or_create(nombre_tiempo=item["section"])

            # Creamos o buscamos la canción por título
            # Si es nueva, asignamos el tiempo litúrgico correspondiente
            cancion, created = Cancion.objects.get_or_create(
                titulo=item["title"],
                defaults={"id_tiempo": tiempo}
            )

            # Por cada línea de la canción (cuerpo), creamos una instancia LineaCancion
            for line in item["body"]:
                LineaCancion.objects.create(
                    cancion=cancion,
                    linea_num=line["line"],       # Número de línea para ordenar
                    tipo_linea=line["type"],      # Tipo (acorde, letra, etc)
                    contenido=line["content"]     # Texto de la línea
                )

        # Mensaje final al terminar la importación
        self.stdout.write(self.style.SUCCESS('Canciones importadas correctamente.'))
