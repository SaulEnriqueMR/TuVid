#   comando para convertir video usando ffmpeg
#   ffmpeg -i videoentrada.algo -r 60 salida.algo
#   comando para obtener thumbnail usando ffmpegthumbnailer
#   ffmpegthumbnailer -i entrada.algo -s tamaño(numero) -t tiempo(porcentaje) -o imagensalida.algo
import uuid
import os
from PIL import Image
from django.conf import settings

rutasCompletas = {
    'reciensubido': settings.MEDIA_ROOT,
    'thumbnails': os.path.join(settings.MEDIA_ROOT, 'thumbnails'),
    'videos': os.path.join(settings.MEDIA_ROOT, 'videos'),
}

def crearNombreAlmacenamiento():
    nombre = str(uuid.uuid1())
    return(nombre)

def convertirVideo(nombreVideoOriginal, nombreAlmacenamiento):
    try:
        nombreVideo = nombreAlmacenamiento + '.mp4'
        rutaOrigen = os.path.join(rutasCompletas.get('reciensubido'), nombreVideoOriginal)
        rutaDestino = os.path.join(rutasCompletas.get('videos'), nombreVideo)
        os.system('ffmpeg -i %s -r 60 %s' % (rutaOrigen, rutaDestino))
        return "formatovalido"
    except:
        return "formatoinvalido"

def obtenerThumbnail(nombreAlmacenamiento):
    nombreVideo = nombreAlmacenamiento + '.mp4'
    nombreThumbnail = nombreAlmacenamiento + '.png'
    rutaOrigenVideo = os.path.join(rutasCompletas.get('videos'), nombreVideo)
    rutaDestinoThumbnail = os.path.join(rutasCompletas.get('thumbnails'), nombreThumbnail)
    os.system('ffmpegthumbnailer -i %s -s 1200 -o %s' % (rutaOrigenVideo, rutaDestinoThumbnail))

def codificarVideo(nombreVideoOriginal, nombreThumbnailOriginal=None):
    nombreAlmacenamiento = crearNombreAlmacenamiento()
    resultadoConversion = convertirVideo(nombreVideoOriginal, nombreAlmacenamiento)
    if resultadoConversion == "formatovalido":
        if nombreThumbnailOriginal is None:
            obtenerThumbnail(nombreAlmacenamiento)
        else:
            resultadoConversionThumbnail = convertirThumbnail(nombreThumbnailOriginal, nombreAlmacenamiento)
            if resultadoConversionThumbnail == "thumbnailinvalida":
                return "formatoinvalido"
        return nombreAlmacenamiento
    else:
        return "formatoinvalido"

def convertirThumbnail(nombreThumbnailOriginal, nombreAlmacenamiento):
    try:
        rutaOrigen = os.path.join(rutasCompletas.get('reciensubido'), nombreThumbnailOriginal)
        nombreConTerminacion = nombreAlmacenamiento + '.png'
        rutaDestino = os.path.join(rutasCompletas.get('thumbnails'), nombreConTerminacion)
        imagen = Image.open(rutaOrigen)
        imagen.save(rutaDestino)
        return "thumbnailvalida"
    except:
        return "thumbnailinvalida"
