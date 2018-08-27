from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import json
from modelos import models
from modelos import modelviews
from modelos import operaciones
import os
import time
from TuVidEnc import videoencoder
from contextlib import contextmanager

ubicacionServidorPrincipal = "http://127.0.0.1:80"

@csrf_exempt
def nuevovideo(request):
    if request.method == 'POST':
        try:
            rutaVideos = os.path.join(settings.MEDIA_URL, 'videos')
            rutaThumnails = os.path.join(settings.MEDIA_URL, 'thumbnails')
            titulo = request.POST.get('titulo')
            fechasubida = time.strftime('%Y-%m-%d %H:%M:%S')
            idcuenta = request.POST.get('idcuenta')
            video = request.FILES.get('video')
            fs = FileSystemStorage()
            nombreTemporalVideo = str(idcuenta) + titulo.replace(" ", "")
            nombreVideo = fs.save(nombreTemporalVideo, video)
            operaciones.crearNotificacion(idcuenta, "Tu video %s ya fue guardado" % (video.name), time.strftime('%Y-%m-%d %H:%M:%S'))
            if 'thumbnail' in request.FILES:
                thumbnail = request.FILES.get('thumbnail')
                nombreTemporalThumbnail = str(idcuenta) + video.name
                nombreThumbnail = fs.save(nombreTemporalThumbnail, thumbnail)
                nombreAlmacenamiento = videoencoder.codificarVideo(nombreTemporalVideo, nombreTemporalThumbnail)
            else:
                nombreAlmacenamiento = videoencoder.codificarVideo(nombreTemporalVideo)
            if nombreAlmacenamiento == "formatoinvalido":
                operaciones.crearNotificacion(idcuenta, "Debes subir un thumbnail o video válidos", time.strftime('%Y-%m-%d %H:%M:%S'))
            else:    
                if 'descripcion' in request.POST:
                    descripcion = request.POST.get('descripcion')
                    resultadoGuardado = operaciones.subirVideo(titulo, fechasubida, idcuenta, os.path.join(rutaVideos, nombreAlmacenamiento + '.mp4'), os.path.join(rutaThumnails, nombreAlmacenamiento + '.png'), descripcion)
                else:
                    resultadoGuardado = operaciones.subirVideo(titulo, fechasubida, idcuenta, os.path.join(rutaVideos, nombreAlmacenamiento + '.mp4'), os.path.join(rutaThumnails, nombreAlmacenamiento + '.png'))
            operaciones.crearNotificacion(idcuenta, "Tu video %s ya puede ser visto por los demás, recarga la página para poder verlo" % (video.name), time.strftime('%Y-%m-%d %H:%M:%S'))    
            return redirect(ubicacionServidorPrincipal)
        except:
            operaciones.crearNotificacion(idcuenta, "Hubo un error al guardar el video %s, vuelve a intentarlo" % (video.name), time.strftime('%Y-%m-%d %H:%M:%S'))
            return redirect(ubicacionServidorPrincipal)

