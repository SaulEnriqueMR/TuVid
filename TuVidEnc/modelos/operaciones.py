from modelos.models import *
from modelos.modelviews import *


def subirVideo(tituloVideo, fechaSubidaVideo, idCuentaVideo, rutaVideo, rutaThumbnail, descripcionVideo=None):
    if not descripcionVideo is None:
        nuevoVideo = Video(titulo=tituloVideo, ubicacionvideo=rutaVideo, ubicacionthumbnail=rutaThumbnail, descripcion=descripcionVideo, fechasubida=fechaSubidaVideo, idcuenta=idCuentaVideo)
    else:
        nuevoVideo = Video(titulo=tituloVideo, ubicacionvideo=rutaVideo, ubicacionthumbnail=rutaThumbnail, fechasubida=fechaSubidaVideo, idcuenta=idCuentaVideo)
    nuevoVideo.save()
    return('videosubido')

def crearNotificacion(idcuentaDestino, mensaje, fecha):
    nuevaNotificacion = Notificacion(
        contenido=mensaje, idcuenta=idcuentaDestino, fechanotificacion=fecha, visto=0)
    nuevaNotificacion.save()
