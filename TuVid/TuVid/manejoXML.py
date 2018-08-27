from lxml import etree
from modelos import operaciones
import uuid
import os
from django.conf import settings

rutaXSDCuenta = os.path.join(settings.STATICFILES_DIRS[0], 'cuenta_schema.xsd')
rutaMedia = settings.MEDIA_ROOT

def crearNombreAlmacenamiento():
    nombre = str(uuid.uuid1())
    return(nombre)

def archivoXMLValido(nombre):
    rutaArchivoXML = os.path.join(rutaMedia, nombre)
    arbolXSD = etree.parse(rutaXSDCuenta)
    xmlEsquema = etree.XMLSchema(arbolXSD)
    archivoXML = etree.parse(rutaArchivoXML)
    if xmlEsquema.validate(archivoXML):
        return(True)
    else:
        return(False)


def importarDesdeXML(nombre):
    dicResultados = {}
    listaErrores = []
    cuentasRegistradas = 0
    cuentasNoRegistradas = 0
    rutaArchivoXML = os.path.join(rutaMedia, nombre)
    try:
        if archivoXMLValido(nombre):
            archivoXML = etree.parse(rutaArchivoXML)
            cuentas = archivoXML.getroot()
            for c in cuentas:
                usuarioIngresado = c[0].text
                contrasenaIngresada = c[1].text
                resultadoRegistroXML = operaciones.registrarCuenta(usuarioIngresado, contrasenaIngresada)
                if resultadoRegistroXML == 'Exito1':
                    cuentasRegistradas += 1
                else:
                    cuentasNoRegistradas += 1
                    if not resultadoRegistroXML in listaErrores:
                        listaErrores.append(resultadoRegistroXML)
        else:
            listaErrores.append('Error6')
    except:
        listaErrores.append('Error6')
    finally:
        dicResultados['cuentasRegistradas'] = cuentasRegistradas
        dicResultados['cuentasNoRegistradas'] = cuentasNoRegistradas
        dicResultados['listaErrores'] = listaErrores
        return(dicResultados)
