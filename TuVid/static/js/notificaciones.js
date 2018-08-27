$(function () {
    var notificaciones = setInterval(function(){ obtenerNotificaciones() }, 500)
        
        
    function obtenerNotificaciones () {
        $.ajax({ url: "/obtenernotificaciones/", success: function(json) {
            $("#numeroNotificaciones").text(json.length);
            notificaciones = "";
            for (var i = 0; i < json.length; i++) {
                $("#n" + (i + 1).toString()).text(json[i].contenido);
                if (json[i].visto === 1 && json[i].contenido.indexOf("guardado") > -1) {
                    cambiarBarraNotificacion("guardado");
                }
                if (json[i].visto === 1 && json[i].contenido.indexOf("verlo") > -1) {
                    cambiarBarraNotificacion("verlo");
                }
                if (json[i].visto === 1 && json[i].contenido.indexOf("error") > -1) {
                    cambiarBarraNotificacion("error");
                }
            }
        }});
    }

    function cambiarBarraNotificacion(palabraClave){
        if($("#barra").length > 0){
            var encabezadoBarra = $("#encabezadoBarra")
            var barraProgreso = $("#barraProgreso");
            switch(palabraClave){
                case "guardado":
                    barraProgreso.css("width", "50%");
                    encabezadoBarra.text("Ya se subió el archivo");
                    break;
                case "verlo":
                    console.log("Llego")
                    barraProgreso.css("width", "99%");
                    encabezadoBarra.text("El video ya puede ser visto, se te redireccionará a la página principal");
                    break;
                case "error":
                    barraProgreso.css("width", "0%");
                    encabezadoBarra.text("Hubo un error, se te redireccionará a la página principal");
                    break;
            }
        }
    }

});