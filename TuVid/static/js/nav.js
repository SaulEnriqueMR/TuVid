$(function () {

    $("#formRegistro").submit(function(event) {
        if ($("#usuarioregistro").val() && $("#contraseniaregistro").val()) {
            return;
        }
        else {
            if ($("#archivoxmlregistro").val()) {
                return;
            }
            else {
                $("#alertaformRegistroVacio").css("display", "block");
                event.preventDefault();
            }
        }
    });

    $("#formBusqueda").submit(function(event) {
        if ($("#terminoBusqueda").val()) {
            return;
        } else {
            event.preventDefault();
        }    
    });

});
