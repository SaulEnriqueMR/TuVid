from __future__ import unicode_literals
from django.db import models

class Thumbnail(models.Model):
    idthumbnail = models.IntegerField(db_column='id', primary_key=True)
    idvideo = models.IntegerField(db_column='idVideo')
    titulo = models.TextField(db_column='titulo')
    ubicacionthumbnail = models.TextField(db_column='ubicacionThumbnail')
    ubicacionvideo = models.TextField(db_column='ubicacionVideo')
    usuario = models.TextField(db_column='usuario')
    visitas = models.IntegerField(db_column='visitas')
    fecha = models.DateField(db_column='fecha')

    class Meta:
        managed = False
        db_table = 'Thumbnail'

class MasVistos(models.Model):
    idmasvistos = models.IntegerField(db_column='id', primary_key=True)
    idvideo = models.IntegerField(db_column='idVideo')
    titulo = models.TextField(db_column='titulo')
    ubicacionthumbnail = models.TextField(db_column='ubicacionThumbnail')
    ubicacionvideo = models.TextField(db_column='ubicacionVideo')
    usuario = models.TextField(db_column='usuario')
    visitas = models.IntegerField(db_column='visitas')
    fecha = models.DateField(db_column='fecha')

    class Meta:
        managed = False
        db_table = 'MasVistos'

class MasBuscados(models.Model):
    idmasbuscados = models.IntegerField(db_column='id', primary_key=True)
    idvideo = models.IntegerField(db_column='idVideo')
    titulo = models.TextField(db_column='titulo')
    ubicacionthumbnail = models.TextField(db_column='ubicacionThumbnail')
    ubicacionvideo = models.TextField(db_column='ubicacionVideo')
    usuario = models.TextField(db_column='usuario')
    visitas = models.IntegerField(db_column='visitas')
    fecha = models.DateField(db_column='fecha')

    class Meta:
        managed = False
        db_table = 'MasBuscados'

class Recientes(models.Model):
    idrecientes = models.IntegerField(db_column='id', primary_key=True)
    idvideo = models.IntegerField(db_column='idVideo')
    titulo = models.TextField(db_column='titulo')
    ubicacionthumbnail = models.TextField(db_column='ubicacionThumbnail')
    ubicacionvideo = models.TextField(db_column='ubicacionVideo')
    usuario = models.TextField(db_column='usuario')
    visitas = models.IntegerField(db_column='visitas')
    fecha = models.DateField(db_column='fecha')

    class Meta:
        managed = False
        db_table = 'Recientes'

class VideoDetalle(models.Model):
    idvideodetalle = models.IntegerField(db_column='id', primary_key=True)
    idvideo = models.IntegerField(db_column='idVideo')
    titulo = models.TextField(db_column='titulo')
    ubicacionthumbnail = models.TextField(db_column='ubicacionThumbnail')
    ubicacionvideo = models.TextField(db_column='ubicacionVideo')
    usuario = models.TextField(db_column='usuario')
    visitas = models.IntegerField(db_column='visitas')
    fecha = models.DateField(db_column='fecha')
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'VideoDetalle'


class NotificacionesOrdenadas(models.Model):
    idnotificacionordenada = models.IntegerField(db_column='id', primary_key=True)
    idnotificacion = models.AutoField(db_column='idNotificacion', primary_key=True)
    contenido = models.CharField(max_length=255)
    idcuenta = models.IntegerField(db_column='idCuenta')
    fechanotificacion = models.DateTimeField(db_column='fechaNotificacion')
    visto = models.IntegerField(db_column='visto')

    class Meta:
        managed = False
        db_table = 'NotificacionesOrdenadas'
