# Generated by Django 5.1.7 on 2025-03-31 17:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cancion',
            fields=[
                ('id_cancion', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TiempoLiturgico',
            fields=[
                ('id_tiempo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tiempo', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ConfiguracionUsuario',
            fields=[
                ('id_usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='canciones.usuario')),
                ('modo_oscuro', models.BooleanField(default=False)),
                ('ultima_tonalidad', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canciones.cancion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canciones.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='LineaCancion',
            fields=[
                ('id_linea', models.AutoField(primary_key=True, serialize=False)),
                ('linea_num', models.IntegerField()),
                ('tipo_linea', models.CharField(max_length=50)),
                ('contenido', models.TextField()),
                ('cancion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canciones.cancion')),
            ],
        ),
        migrations.CreateModel(
            name='ListaPersonal',
            fields=[
                ('id_lista', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_lista', models.CharField(max_length=255)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canciones.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='ListaCancion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canciones.cancion')),
                ('lista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canciones.listapersonal')),
            ],
        ),
        migrations.AddField(
            model_name='cancion',
            name='id_tiempo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='canciones.tiempoliturgico'),
        ),
    ]
