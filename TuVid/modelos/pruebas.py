from modelos import operaciones

def pruebasCuenta():
    numeroPruebasPasadas = 0

    registroCuentaRepetida = operaciones.registrarCuenta("usuario", "contraseña")
    if registroCuentaRepetida == 'existeusuario':
        numeroPruebasPasadas += 1

    registroCuentaNormal = operaciones.registrarCuenta("cuentainexistente", "contraseña")
    if registroCuentaNormal == 'cuentaregistrada':
        numeroPruebasPasadas += 1
    
    inicioMalUsuario = operaciones.iniciarSesion("usuario11000", "contraseña")
    if inicioMalUsuario == "noexisteusuario":
        numeroPruebasPasadas += 1

    inicioMalContrasenia = operaciones.iniciarSesion("usuario", "contrasenia")
    if inicioMalContrasenia == "contraseniaincorrecta":
        numeroPruebasPasadas += 1
    
    inicioBien = operaciones.iniciarSesion("usuario", "contraseña")
    if inicioBien == "inicioexito":
        numeroPruebasPasadas += 1
    
    obtenerBienID = operaciones.obtenerIdCuentaIniciada("saule", "saule")
    if obtenerBienID == 1:
        numeroPruebasPasadas += 1
    
    return numeroPruebasPasadas
    
    
numeroPruebasPasadas = pruebasCuenta()
if numeroPruebasPasadas == 6:
    print("Todas las pruebas pasaron")
else:
    print("Pasaron %s de 6 pruebas" % (numeroPruebasPasadas))