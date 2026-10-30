
//prueba local para verificar llamado a JS
//alert("Conexion con JS"); 


class VistaRecoleccion{
//Esta funcion obtiene los valores de HTML, getElementById es una funcion de JS en el navegador
 iniciar() {

    var vista = this

    document.getElementById("ciudad").onchange = function(){vista.ciudad()};
    document.getElementById("generar").onclick = function(){vista.generar()};
    document.getElementById("calcular").onclick = function(){vista.calcular()};
    document.getElementById("tipo").onchange = function(){vista.mostrarRuta()};
    document.getElementById("optimizar").onclick = function(){vista.optimizar()};
    document.getElementById("reiniciar").onclick = function(){vista.reiniciar()};
    
    this.ciudad();
}
// Coloca un tamaño default para las ciudades precargadas
 ciudad() {

    var ciudad = document.getElementById("ciudad").value;
    if (ciudad == "1") {
        document.getElementById("filas").value = 10;
        document.getElementById("columnas").value = 10;
    }
    else if (ciudad == "2") {
        document.getElementById("filas").value = 8;
        document.getElementById("columnas").value = 10;
    }
    else {
        document.getElementById("filas").value = 10;
        document.getElementById("columnas").value = 8;
    }
}



// Envía los datos de la ventana de captura hacia Python para generar la malla
async  generar() {

    var filas = document.getElementById("filas").value;
    var columnas = document.getElementById("columnas").value;
    var organicos = document.getElementById("organicos").value;
    var reciclables = document.getElementById("reciclables").value;
    var noReciclables = document.getElementById("no-reciclables").value;

    //pywebview es la libreria utilizada para renderizar el html desde python
    var respuesta = await window.pywebview.api.generar_escenario(
        filas,
        columnas,
        organicos,
        reciclables,
        noReciclables
    );
    document.getElementById("mensaje").innerText = respuesta.mensaje;
    if (respuesta.ok == true) {
        this.mostrarMalla(respuesta.datos);
    }
}
/// Muestra los puntos de la malla dentro de una tabla HTML
 mostrarMalla(escenario) {

    var tabla = document.getElementById("tabla-malla"); //busca tabla donde se mostrará la malla
    tabla.innerHTML = "";

    var letras = ["", "O", "R", "NR"];
    //filas
    for (var fila = 1; fila <= escenario.filas; fila++) {
        //renglon html
        var renglon = document.createElement("tr");
        for (var columna = 1; columna <= escenario.columnas; columna++) {
            //celda html
            var celda = document.createElement("td");
            var texto = "";
            //valida si existe puntos
            for (var i = 0; i < escenario.puntos.length; i++) {
                var punto = escenario.puntos[i];
                if (punto.x == fila && punto.y == columna) {
                    texto = "P" + punto.id;
                    if (punto.tipos_residuo.length == 1) {
                        var tipoColor = punto.tipos_residuo[0].id;
                        if (tipoColor == 1) {
                            celda.classList.add("organico");
                        }
                        else if (tipoColor == 2) {
                            celda.classList.add("reciclable");
                        }
                        else {
                            celda.classList.add("no-reciclable");
                        }
                    }
                    //agrega tipos de residuo
                    for (var j = 0; j < punto.tipos_residuo.length; j++) {
                        var tipo = punto.tipos_residuo[j].id;
                        texto = texto + ":" + letras[tipo];
                    }
                }
            }
            //se agrega texto dentro de la celda
            celda.innerText = texto;
            //agrega celda al renglon
            renglon.appendChild(celda);
        }
        //agrega renglon a la tabla
        tabla.appendChild(renglon);
    }
}


//Indica calcular las rutas, manda llamar la función de python mediante pywebview
async  calcular() {

    var respuesta = await window.pywebview.api.calcular_rutas();
    document.getElementById("mensaje").innerText = respuesta.mensaje;
    if (respuesta.ok == true) {
        this.mostrarRuta();
    }
}


///Muestra las rutas, manda llamar la función de python mediante pywebview
async  mostrarRuta() {

    var tipo = document.getElementById("tipo").value;
    var respuesta = await window.pywebview.api.consultar_ruta(tipo);
    document.getElementById("mensaje").innerText = respuesta.mensaje;
    var texto = ""
    if (respuesta.ok == true) {

        var ruta = respuesta.datos;
        var textoRuta = "";
        for (var i = 0; i < ruta.puntos.length; i++) {
            if (i > 0) {
                textoRuta = textoRuta + " > ";
            }

        textoRuta = textoRuta + "P" + ruta.puntos[i].id;
}

if (textoRuta == "") {
    textoRuta = "Sin puntos";
}
        texto = texto + "Residuo: " + ruta.nombre_residuo + "\n";
        texto = texto + "Camión: " + ruta.id_camion + "\n";
        texto = texto + "Ruta: " + textoRuta + "\n";
        texto = texto + "Distancia: " + ruta.distancia_total.toFixed(2) + " km\n";
        texto = texto + "Tiempo: " + ruta.tiempo_minutos.toFixed(2) + " minutos";

        document.getElementById("informacion-ruta").innerText = texto;
    }
}
// Solicita a Python la ruta optimizada mediante pywebview
async  optimizar() {

    var tipo = document.getElementById("tipo").value;
    var respuesta = await window.pywebview.api.optimizar_ruta(tipo);
    
    document.getElementById("mensaje").innerText = respuesta.mensaje;

    if (respuesta.ok == true) {

        var datos = respuesta.datos;
        var ruta = datos.ruta_optimizada;
        var texto = "";
        var textoRuta = "";

        for (var i = 0; i < ruta.puntos.length; i++) {
            if (i > 0) {
                textoRuta = textoRuta + " > ";
            }
            textoRuta = textoRuta + "P" + ruta.puntos[i].id;
        }
        if (textoRuta == "") {
        textoRuta = "Sin puntos";
    }
         texto = texto + "Residuo: " + ruta.nombre_residuo + "\n";
        texto = texto + "Camión: " + ruta.id_camion + "\n";
        texto = texto + "Ruta: " + textoRuta + "\n";
        texto = texto + "Distancia: " + datos.distancia_optimizada.toFixed(2) + " km\n";
        texto = texto + "Tiempo: " + ruta.tiempo_minutos.toFixed(2) + " minutos";
        document.getElementById("informacion-optimizada").innerText = texto;
    }
}

// Reinicia la aplicación
async  reiniciar() {

    var respuesta = await window.pywebview.api.reiniciar();
    document.getElementById("mensaje").innerText = respuesta.mensaje;
    if (respuesta.ok == true) {

        document.getElementById("tabla-malla").innerHTML = "";
        document.getElementById("informacion-ruta").innerText =
            "Sin ruta calculada";

        document.getElementById("informacion-optimizada").innerText =
            "Sin optimización";

        this.ciudad();
      }
    }
}

var vista = new VistaRecoleccion();

//  pywebview conexión de JavaScript - Python
if (window.pywebview && window.pywebview.api) {
    vista.iniciar();
}
else {
    window.addEventListener("pywebviewready", function(){vista.iniciar();});
}


