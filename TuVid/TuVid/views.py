from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import json
from modelos import models
from modelos import operaciones
import os
import time
from TuVid import manejoXML

direccionServidorVideo = "http://127.0.0.1:81"

listaMensajes = {
    "errordesconocido": "Error desconocido",
    "existeusuario": "Ya existe una cuenta con ese usuario",
    "noexisteusuario": "Ese usuario no existe",
    "contraseniaincorrecta": "Contraseña incorrecta",
    "nosubirnosesion": "No puedes subir un video porque no has iniciado sesión",
    "formregistroinvalido": "Debe registrar un usuario y una contraseña o importar un archivo xml con el usuario y la contraseña",
    "formatoxmlinvalido": "Formato XML inválido, debe seguir la sintáxis <cuentas><cuenta><usuario></usuario><contrasenia></contrasenia></cuenta></cuentas>",
    "errorguardarvideo": "Hubo un error al guardar el vídeo, vuelva a intentarlo",
    "videonoexiste": "El video al que intentó acceder no existe",
    "noterminobusqueda": "Debe insertar un termino de busqueda para buscar",
    "nousuarionocontrasenia": "Debe ingresar usuario y contraseña para iniciar sesion",
    "cuentaregistrada": "Cuenta registrada exitosamente",
    "inicioexito": "Inicio de sesión exitoso",
    "cuentasxmlregistradas": "Se registraron las cuentas XML",
    "videosubido": "Vídeo subido exitosamente",
}

def index(request):
    argumentos = {}
    if 'sesionIniciada' in request.session:
        argumentos['sesionIniciada'] = True
    if 'error' in request.session:
        argumentos['error'] = request.session.get('error')
        del request.session['error']
    if 'mensaje' in request.session:
        argumentos['mensaje'] = request.session.get('mensaje')
        del request.session['mensaje']
    if 'listaErrores' in request.session:
        argumentos['listaErrores'] = request.session.get('listaErrores')
        del request.session['listaErrores']
    if 'buscando' in request.session:
        del request.session['buscando']
    recientes = operaciones.obtenerRecientes()
    masVistos = operaciones.obtenerMasVistos()
    masBuscados = operaciones.obtenerMasBuscados()
    argumentos['recientes'] = recientes
    argumentos['masvistos'] = masVistos
    argumentos['masbuscados'] = masBuscados
    argumentos['direccionServidorVideo'] = direccionServidorVideo
    return render(request, 'index.html', argumentos)

def registrarcuenta(request):
    listaErrores = []
    if request.method == 'POST':
        if 'usuario' in request.POST and 'contrasenia' in request.POST:
            usuario = request.POST.get('usuario')
            contrasenia = request.POST.get('contrasenia')
            if not usuario == "" and not contrasenia == "":
                resultadoRegistro = operaciones.registrarCuenta(usuario, contrasenia)
                if resultadoRegistro is "errordesconocido" or resultadoRegistro is "existeusuario":
                    request.session['error'] = True
                    request.session['mensaje'] = listaMensajes.get(resultadoRegistro)
                else:
                    request.session['error'] = False
                    request.session['mensaje'] = listaMensajes.get(resultadoRegistro)
            else:
                archivoXML = request.FILES['archivoxml']
                fs = FileSystemStorage()
                nombreAlmacenamiento = manejoXML.crearNombreAlmacenamiento()
                nombreAlmacenamiento += '.xml'
                nombreArchivo = fs.save(nombreAlmacenamiento, archivoXML)
                resultadoImportacion = manejoXML.importarDesdeXML(nombreAlmacenamiento)
                if not resultadoImportacion['listaErrores']:
                    request.session['error'] = False
                    request.session['mensaje'] = listaMensajes.get('cuentasxmlregistradas')
                else:
                    for error in resultadoImportacion.get('listaErrores'):
                        listaErrores.append(listaMensajes.get(error))
                    request.session['error'] = True
                    request.session['mensaje'] = "Se importaron %s cuentas, no se importaron %s cuentas por las siguientes razones:" % (str(resultadoImportacion.get('cuentasRegistradas')), str(resultadoImportacion.get('cuentasNoRegistradas')))
                    request.session['listaErrores'] = listaErrores             
        else:
            request.session['error'] = True
            request.session['mensaje'] = listaMensajes.get('formregistroinvalido')
    return redirect('/')

def iniciarsesion(request):
    if request.method == 'POST':
        if 'usuario' in request.POST and 'contrasenia' in request.POST:
            usuario = request.POST.get('usuario')
            contrasenia = request.POST.get('contrasenia')
            resultadoInicio = operaciones.iniciarSesion(usuario, contrasenia)
            if resultadoInicio is "noexisteusuario" or resultadoInicio is "contraseniaincorrecta":
                request.session['error'] = True
                request.session['mensaje'] = listaMensajes.get(resultadoInicio)
            else:
                request.session['error'] = False
                request.session['sesionIniciada'] = True
                request.session['idcuenta'] = operaciones.obtenerIdCuentaIniciada(usuario, contrasenia)
        else:
            request.session['error'] = True
            request.session['mensaje'] = listaMensajes.get('nousuarionocontrasenia')
    return redirect('/')

def cerrarsesion(request):
    if 'sesionIniciada' in request.session:
        del request.session['sesionIniciada']
        del request.session['idcuenta']
    if 'buscando' in request.session:
        del request.session['buscando']
    return redirect('/')

def subirvideo(request):
    argumentos = {}
    if 'sesionIniciada' in request.session:
        argumentos['sesionIniciada'] = request.session.get('sesionIniciada')
        argumentos['idcuenta'] = request.session.get('idcuenta')
        if 'buscando' in request.session:
            del request.session['buscando']
        argumentos['direccionServidorVideo'] = direccionServidorVideo
        return render(request, 'subirvideo.html', argumentos)
    else:
        request.session['error'] = True
        request.session['mensaje'] = listaMensajes.get("nosubirnosesion")
        return redirect('/')

def vervideo(request, *args, **kwargs):
    argumentos = {}
    if 'idvideo' in kwargs:
        idvideo = kwargs.get('idvideo')
        listaVideos = operaciones.obtenerVideoDetalle(idvideo)
        if listaVideos:
            argumentos['video'] = listaVideos[0]
            if 'idcuenta' in request.session:
                operaciones.registrarInteraccion(listaVideos[0].idvideo, 1, request.session.get('idcuenta'))
                if 'buscando' in request.session:
                    operaciones.registrarInteraccion(listaVideos[0].idvideo, 2, request.session.get('idcuenta'))
            else:
                operaciones.registrarInteraccion(listaVideos[0].idvideo, 1)
                if 'buscando' in request.session:
                    operaciones.registrarInteraccion(listaVideos[0].idvideo, 2)
            argumentos['direccionServidorVideo'] = direccionServidorVideo
            argumentos['sesionIniciada'] = request.session.get('sesionIniciada')
            argumentos['idcuenta'] = request.session.get('idcuenta')
            return render(request, 'vervideo.html', argumentos)
        else:
            request.session['error'] = True
            request.session['mensaje'] = listaMensajes.get("videonoexiste")
            return redirect('/')
    else:
        redirect('/')
    if 'buscando' in request.session:
        del request.session['buscando']
    argumentos['direccionServidorVideo'] = direccionServidorVideo
    return render(request, 'vervideo.html', argumentos)

def buscar(request, *args, **kwargs):
    argumentos = {}
    if 'terminobusqueda' in request.GET:
        terminoBusqueda = request.GET.get('terminobusqueda')
        resultadoBusqueda = operaciones.buscar(terminoBusqueda)
        argumentos['resultadobusqueda'] = resultadoBusqueda
        request.session['buscando'] = True
        argumentos['sesionIniciada'] = request.session.get('sesionIniciada')
        argumentos['idcuenta'] = request.session.get('idcuenta')
        argumentos['direccionServidorVideo'] = direccionServidorVideo
        return render(request, 'buscar.html', argumentos)
    else:
        request.session['error'] = True
        request.session['mensaje'] = listaMensajes.get('noterminobusqueda')
        return redirect('/')

def obtenernotificaciones(request):
    if 'idcuenta' in request.session:
        idcuenta = request.session.get('idcuenta')
        notificaciones = operaciones.obtenerNotificaciones(idcuenta)
        notificacionesSerializadas = [ serializadornotificaciones(notificacion) for notificacion in notificaciones ]
        return HttpResponse(json.dumps(notificacionesSerializadas), content_type='application/json')
    else:
        notificacionesNulas = {'contenido': 'vacio'}
        return HttpResponse(json.dumps(notificacionesNulas), content_type='application/json; encoding=utf-8')

def serializadornotificaciones(notificacion):
    return {'contenido': notificacion.contenido, 'visto': notificacion.visto}
