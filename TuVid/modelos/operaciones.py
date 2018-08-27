from modelos.models import *
from modelos.modelviews import *

def registrarCuenta(usuarioIngresado, contrasenaIngresada):
    listaCuentas = Cuenta.objects.filter(usuario=usuarioIngresado)
    if listaCuentas:
        return("existeusuario")
    else:
        try:
            nuevaCuenta = Cuenta(usuario=usuarioIngresado, contrasenia=contrasenaIngresada)
            nuevaCuenta.save()
            return("cuentaregistrada")
        except:
            return("errordesconocido")

def iniciarSesion(usuarioIngresado, contrasenaIngresada):
    listaCuentas = Cuenta.objects.filter(usuario=usuarioIngresado)
    if listaCuentas:
        cuenta = listaCuentas[0]
        if cuenta.contrasenia == contrasenaIngresada:
            return("inicioexito")
        else:
            return("contraseniaincorrecta")
    else:
        return("noexisteusuario")

def obtenerIdCuentaIniciada(usuarioIngresado, contrasenaIngresada):
    cuentaObtenida = Cuenta.objects.get(usuario=usuarioIngresado, contrasenia=contrasenaIngresada)
    return(cuentaObtenida.idcuenta)

def subirVideo(tituloVideo, fechaSubidaVideo, idCuentaVideo, rutaVideo, rutaThumbnail, descripcionVideo=None):
    if not descripcionVideo is None:
        nuevoVideo = Video(titulo=tituloVideo, ubicacionvideo=rutaVideo, ubicacionthumbnail=rutaThumbnail, descripcion=descripcionVideo, fechasubida=fechaSubidaVideo, idcuenta=idCuentaVideo)
    else:
        nuevoVideo = Video(titulo=tituloVideo, ubicacionvideo=rutaVideo, ubicacionthumbnail=rutaThumbnail, fechasubida=fechaSubidaVideo, idcuenta=idCuentaVideo)
    nuevoVideo.save()
    return('videosubido')

def obtenerRecientes():
    videosRecientes = Recientes.objects.all()[:5]
    return videosRecientes

def obtenerMasBuscados():
    masBuscados = MasBuscados.objects.all()[:5]
    return masBuscados

def obtenerMasVistos():
    masVistos = MasVistos.objects.all()[:5]
    return masVistos

def obtenerVideoDetalle(idVideoPorBuscar):
    listaVideos = VideoDetalle.objects.filter(idvideo=idVideoPorBuscar)
    return listaVideos

def registrarInteraccion(idVideoInteractuado, idTipoInteraccion, idCuentaInteractua=None):
    if not idCuentaInteractua is None:
        nuevaInteraccion = Interaccion(idcuenta=idCuentaInteractua, idvideo=idVideoInteractuado, idtipointeraccion=idTipoInteraccion)
    else:
        nuevaInteraccion = Interaccion(idvideo=idVideoInteractuado, idtipointeraccion=idTipoInteraccion)
    nuevaInteraccion.save()

def buscar(terminoBusqueda):
    resultados = []
    titulosRelacionados = Video.objects.filter(titulo__icontains=terminoBusqueda)
    if titulosRelacionados:
        for titulo in titulosRelacionados:
            resultados.append(titulo.idvideo)
    descripcionesSimilares = Video.objects.filter(descripcion__icontains=terminoBusqueda)[:10]
    if descripcionesSimilares:
        for descripcion in descripcionesSimilares:
            if not descripcion in resultados:
                resultados.append(descripcion.idvideo)
    cuentaConEseUsuario = Cuenta.objects.filter(usuario__icontains=terminoBusqueda)[:5]
    if cuentaConEseUsuario:
        for cuenta in cuentaConEseUsuario:
            videosDeEsaCuenta = Video.objects.filter(idcuenta=cuenta.idcuenta)[:5]
            for video in videosDeEsaCuenta:
                if not video in resultados:
                    resultados.append(video.idvideo)
    resultadoBusqueda = []
    if resultados:
        for resultado in resultados:
            thumbnail = Thumbnail.objects.get(idvideo=resultado)
            resultadoBusqueda.append(thumbnail)
    return resultadoBusqueda

def crearNotificacion(idcuentaDestino, mensaje, fecha):
    nuevaNotificacion = Notificacion(contenido=mensaje, idcuenta=idcuentaDestino, fechanotificacion=fecha, visto=0)
    nuevaNotificacion.save()

def obtenerNotificaciones(idCuentaConsulta):
    notificaciones = NotificacionesOrdenadas.objects.filter(idcuenta=idCuentaConsulta)[:5]
    for notificacion in notificaciones:
        notificacionAModificar = Notificacion.objects.get(idnotificacion=notificacion.idnotificacion)
        if notificacionAModificar.visto == 0:
            notificacionAModificar.visto = 1
            notificacionAModificar.save()
    return notificaciones
