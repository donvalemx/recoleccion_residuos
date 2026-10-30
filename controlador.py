import modelos as modelo

class ControladorRecoleccion:
    def __init__(self):
        self.ciudad = None
        self.camiones = {}
        self.rutas = {}

    #Recibe los valores seleccionados desde la vista HTML
    def generar_escenario(self, filas=None, columnas=None, cantidad_organicos=None,cantidad_reciclables=None, cantidad_no_reciclables=None,seed=None):
        try:
            # El formulario envía textos, no se acepta decimales ni campos vacíos
            filas = int(str(filas))
            columnas = int(str(columnas))
            organicos = int(str(cantidad_organicos))
            reciclables = int(str(cantidad_reciclables))
            no_reciclables = int(str(cantidad_no_reciclables))
            if seed is not None:
                seed = int(str(seed))
            malla = modelo.CiudadMalla(filas, columnas) #manda generar la malla desde el modelo
            malla.ubicarPuntosRecoleccion(organicos, reciclables, no_reciclables, seed) #localiza los puntos en la malla, esta función en el modelo es clave
       
        except modelo.ErrorMalla as error: #Excepcion de Modelo
            return self.respuesta(False, "Ocurrió un error al generar la malla : " + str(error))
        except ValueError as error:
            return self.respuesta(False, "Revise que los números sean enteros : " + str(error)) 
       
        #Se manda llamar crear la ciudad, se asigna su malla, camion y operador
        self.ciudad = modelo.Ciudad("Ciudad Universitaria", malla) #se establece un valor constante
        self.rutas = {}
        self.camiones = {}
        for tipo_residuo in modelo.TipoResiduo:
            camion = modelo.Camion(tipo_residuo.value, tipo_residuo)
            operador = modelo.OperadorCamion(tipo_residuo.value, "Operador " + str(tipo_residuo.value))
            operador.asignarCamion(camion)
            self.camiones[tipo_residuo] = camion
       
        #Prepara los puntos de la malla para mandarlos a la vista de retorno
        puntos_recoleccion = []
        for punto in malla.mostrarMalla():
            puntos_recoleccion.append(self.datos_punto(punto))
        #se crea und diccionario con filas, columnas y puntos para que sea dibujado en la malla
        valores_malla = {"filas": filas, "columnas": columnas, "puntos": puntos_recoleccion}
        return self.respuesta(True, "Puntos generados. Ahora calcule las rutas", valores_malla)

    def calcular_rutas(self):
        #Si no existe ciudad no puede avanzar e indica generar la malla
        if self.ciudad is None:
            return self.respuesta(False, "Primero genere los puntos")
        #Si no existen rutas, por cada tipo de resiudo las genera y asigna
        if len(self.rutas) == 0:
            for tipo in modelo.TipoResiduo:
                ruta = modelo.RutaRecoleccion(tipo.value, tipo, [])
                ruta.calcularRuta(self.ciudad.malla.mostrarMalla())
                self.camiones[tipo].asignarRuta(ruta)
                self.rutas[tipo] = ruta
        #Si ya genero las 3 rutas devuelve los valores para su consulta.
        return self.consultar_rutas()

   
    #Recibe valores y verifica que existan las rutas, las prepara y envia a la vista
    def consultar_rutas(self):
        if len(self.rutas) == 0:
            return self.respuesta(False, "Primero calcule rutas")
        else:
            rutas = []
            for ruta in self.rutas.values():
                rutas.append(self.datos_ruta(ruta))
            return self.respuesta(True, "Tres rutas calculadas", {"rutas": rutas})

    #Filtra y regresa una ruta individual de acuerdo a la seleccionada en la vista
    def consultar_ruta(self, tipo_residuo=None):
        if len(self.rutas) == 0:
            return self.respuesta(False, "Primero calcule las rutas")
        
        tipo = modelo.TipoResiduo(int(str(tipo_residuo)))
        ruta = self.camiones[tipo].consultarRuta()
        
        return self.respuesta(True, "Ruta original.", self.datos_ruta(ruta))

    def optimizar_ruta(self, tipo_residuo=None):
        consulta = self.consultar_ruta(tipo_residuo)
        if consulta["ok"] == False:
            return consulta
        else:
            tipo = modelo.TipoResiduo(int(str(tipo_residuo)))
            original = self.rutas[tipo]
            candidata = original.optimizarRuta()
            diferencia = original.distanciaTotal - candidata.distanciaTotal
            if diferencia > 0:
                mejora = True
                recomendada = candidata
            else:
                mejora = False
                recomendada = original
            datos = {
                "ruta_original": self.datos_ruta(original),
                "ruta_optimizada": self.datos_ruta(candidata),
                "ruta_recomendada": self.datos_ruta(recomendada),
                "distancia_original": original.distanciaTotal,
                "distancia_optimizada": candidata.distanciaTotal,
                "diferencia": diferencia,
                "mejora": mejora
        }
        return self.respuesta(True, "Vecino más cercano: no garantiza el óptimo global", datos)

    def reiniciar(self):
        self.ciudad = None
        self.camiones = {}
        self.rutas = {}
        return self.respuesta(True, "Genere los puntos para comenzar")

    #PYWEBVIEW 
    #Diccionarios para envio de datos a pywebview, simulando respuesta tipo API
   
   #Es una respuesta para mandar a la vista, se necesita para saber si fue exitosa o no
    def respuesta(self, ok, mensaje, datos=None):
        return {"ok": ok, "mensaje": mensaje, "datos": datos}

    #prepara los datos para enviarlos a la vista mediante pywebview
    #este diccionario simula un respuesta en formato JSON que recibe la vista desde el controlador
    def datos_punto(self, punto):
        tipos = []
        for tipo in modelo.TipoResiduo:
            if punto.contiene_tipo(tipo):
                tipos.append({"id": tipo.value, "nombre": tipo.nombre})
        return {"id": punto.id_punto, "x": punto.filax, "y": punto.columnay,
                "tipos_residuo": tipos}

    #Prepara todos los datos de la ruta para envuarlos a la vista a través de pywebview
    def datos_ruta(self, ruta):
        puntos = []
        for punto in ruta.mostrarRuta():
            puntos.append(self.datos_punto(punto))
        tramos_de_ruta = [] #guarda los tramos de ruta entre puntos : modelos.RutaRecoleccion.calcularDistancia()
        for indice in range(len(ruta.puntos) - 1):
            origen = ruta.puntos[indice]
            destino = ruta.puntos[indice + 1]
            distancia = ruta.calcularDistancia(origen, destino)
            tramos_de_ruta.append({"origen": self.datos_punto(origen), "destino": self.datos_punto(destino),"distancia": distancia})
        return {
            "id_ruta": ruta.idRuta,
            "id_camion": self.camiones[ruta.tipoResiduo].idCamion,
            "tipo_residuo": ruta.tipoResiduo.value,
            "nombre_residuo": ruta.tipoResiduo.nombre,
            "puntos": puntos,
            "segmentos": tramos_de_ruta,
            "cantidad_puntos": len(ruta.puntos),
            "distancia_total": ruta.distanciaTotal,
            "tiempo_horas": ruta.tiempoTotal,
            "tiempo_minutos": ruta.tiempoTotal * 60
        }
