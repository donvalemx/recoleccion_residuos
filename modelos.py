from enum import Enum
import math
import random


#Clase para manejo de excepciones
class ErrorMalla(Exception):
    pass

class TipoResiduo(Enum):
    ORGANICO = 1
    INORGANICO_RECICLABLE = 2
    INORGANICO_NO_RECICLABLE = 3

    def __init__(self, numero):
        if numero == 1:
            self.nombre = "Orgánico"
        elif numero == 2:
            self.nombre = "Inorgánico reciclable"
        else:
            self.nombre = "Inorgánico no reciclable"

class Ciudad:
    def __init__(self, nombre, malla, pais="México", coordenadas="Ciudad simulada"):
        self.registrarCiudad(nombre, pais, coordenadas)
        self.malla = malla

    def registrarCiudad(self, nombre, pais, coordenadas):
        self.nombre = nombre
        self.pais = pais
        self.coordenadas = coordenadas

class CiudadMalla:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.puntosRecoleccion = []
        self.generarMalla()

    def validarTamañoMalla(self):
        cantidad_celdas = self.filas * self.columnas
        if cantidad_celdas > 100:
            raise ErrorMalla("La malla admite hasta 100 celdas")
        return True

    def generarMalla(self):
        self.validarTamañoMalla()
        # Las filas y columnas delimitan la malla solo se almacenan sus puntos.
        self.puntosRecoleccion = []

    def mostrarMalla(self):
        return self.puntosRecoleccion

    #LOCALIZACION DE PUNTOS EN MALLA
    def ubicarPuntosRecoleccion(self, organicos, reciclables, no_reciclables, seed=None):
        qty_tipo_residuo = [organicos, reciclables, no_reciclables]
        self.generarMalla() #inicializa la malla para colocar los puntos
        aleatorio = random.Random(seed) 
        indice_tipo = 0 

        #Se totaliza la el total de puntos por cada resiudo. Ejemplo Organico = 3 puntos, reciclables = 3 puntos, no_reciclables = 2 puntos.
        for tipo in TipoResiduo:
            total_qty_tipos = qty_tipo_residuo[indice_tipo]
            contador = 0

            #Se evalua el total de puntos por cada tipo de residudo y se genear puntos aleatorios
            while contador < total_qty_tipos:
                fila= aleatorio.randint(1, self.filas)
                columna= aleatorio.randint(1, self.columnas)
                punto_encontrado = None    #variable para verificar si el punto del residuo en evaluación ya ha sido ubicado                                     

                #Se busca si el punto ya ha sido colocado en la malla
                for punto in self.puntosRecoleccion:
                    if punto.filax == fila and punto.columnay == columna:
                        punto_encontrado= punto
                
                #Si el punto no se encontró se agrega
                if punto_encontrado is None:
                    numero= len(self.puntosRecoleccion) + 1
                    punto_encontrado = PuntoRecoleccion(numero, fila, columna, [])
                    self.puntosRecoleccion.append(punto_encontrado)
                    
                #Si el punto encontrado no tiene tipo de residuo se le agrega
                if punto_encontrado.contiene_tipo(tipo)== False:
                    punto_encontrado.agregarResiduo(tipo)
                    contador= contador + 1
            indice_tipo = indice_tipo + 1

class PuntoRecoleccion:
    def __init__(self, id_punto, filax, columnay, tipos_residuo):
        self.id_punto = id_punto
        # Son las dos componentes de coordenadas en el UML
        self.filax = filax
        self.columnay = columnay
        self.tipos_residuo = set(tipos_residuo)
        self.activo = True
        self.prioridad = "Normal"

    def agregarResiduo(self, tipo):
        if tipo not in self.tipos_residuo:
            self.tipos_residuo.add(tipo)

    def eliminarResiduo(self, tipo):
        if tipo in self.tipos_residuo:
            self.tipos_residuo.remove(tipo)

    def contiene_tipo(self, tipo):
        if tipo in self.tipos_residuo:
            return True
        else:
            return False

class RutaRecoleccion:
    def __init__(self, idRuta, tipoResiduo, puntos):
        self.idRuta = idRuta
        self.tipoResiduo = tipoResiduo
        self.puntos = puntos #puntos se agrega, UML original no lo consideró
        self.distanciaTotal = 0.0
        self.tiempoTotal = 0.0

    def calcularRuta(self, puntosRecoleccion):
        self.puntos = []
        #Para cada punto se revisa si esta activo y si tiene un tipo de resiudo, se agrega en la lista para calcular su tiempo
        for punto in puntosRecoleccion:
            if punto.activo and punto.contiene_tipo(self.tipoResiduo):
                self.puntos.append(punto)
        self.calcularTiempoTotal()
        return self.puntos

    #Se obtiene la distancia euclidiana entre dos puntos
    #Se agrega método, diagrama UML original no lo contemplaba
    def calcularDistancia(self, origen, destino):
        
        diferencia_x = destino.filax - origen.filax
        diferencia_y = destino.columnay - origen.columnay
        distancia = math.sqrt((diferencia_x * diferencia_x) + (diferencia_y * diferencia_y))
        return distancia

    #Calcula la distancia total entre todos los puntos
    def calcularDistanciaTotal(self):
        self.distanciaTotal = 0.0
        for indice in range(len(self.puntos) - 1): #se crea una lista de valores y se evalua como indice para sumar las rutas
            origen= self.puntos[indice] #punto de inicio
            destino = self.puntos[indice + 1] #punto final de comparacion
            distancia= self.calcularDistancia(origen, destino) #se manda llamar el calculo de la distancia
            self.distanciaTotal= self.distanciaTotal + distancia
        return self.distanciaTotal

    def calcularTiempoTotal(self):
        # Ruta constante a 30 km/h. Tiempo = distancia/velocidad
        distancia= self.calcularDistanciaTotal()
        self.tiempoTotal= distancia / 30
        return self.tiempoTotal


    #Optimizar ruta, crea una lista vacia para la nueva ruta y los puntos
    def optimizarRuta(self):
        nueva_ruta = []
        puntos_pendientes = []
          # Si existen puntos el primero se utiliza como inicio de la nueva ruta
        if len(self.puntos) > 0:
            nueva_ruta.append(self.puntos[0])

             # puntos pendientes de recorrer
            for indice in range(1, len(self.puntos)):
                puntos_pendientes.append(self.puntos[indice])
         # Mientras existan puntos pendientes se busca el más cercano
        while len(puntos_pendientes) > 0:
            punto_actual = nueva_ruta[len(nueva_ruta) - 1]
            distancia_menor = None
            punto_cercano = None
            for punto in puntos_pendientes:
                distancia = self.calcularDistancia(punto_actual, punto)
                if distancia_menor is None or distancia < distancia_menor:
                    distancia_menor = distancia
                    punto_cercano = punto
                elif distancia == distancia_menor: # Si existen dos puntos con la misma distancia se selecciona el menor ID
                    if punto.id_punto < punto_cercano.id_punto:
                        punto_cercano = punto
            nueva_ruta.append(punto_cercano)
            puntos_pendientes.remove(punto_cercano)

        # Otra ruta permite comparar sin modificar el recorrido original.
        candidata = RutaRecoleccion(self.idRuta, self.tipoResiduo, nueva_ruta)
        candidata.calcularTiempoTotal()
        return candidata

    def mostrarRuta(self):
        return self.puntos


class OperadorCamion:
    def __init__(self, idOperador, nombre, licencia="", nivelOperador="General"):
        self.idOperador = idOperador
        self.nombre = nombre
        self.licencia = licencia
        self.nivelOperador = nivelOperador

    def asignarCamion(self, camion):
        camion.asignarOperador(self)


class Camion:
    def __init__(self, idCamion, tipoResiduo, serie="", modelo="", año=""):
        self.idCamion = idCamion
        self.idRuta = None
        self.serie = serie
        self.modelo = modelo
        self.año = año
        self.activo = True
        self.idOperador = None
        self.tipoResiduo = tipoResiduo
        self.operador = None
        self.ruta = None

    def asignarRuta(self, ruta):
        if ruta is None:
            self.ruta = None
            self.idRuta = None
        else:
            self.ruta = ruta
            self.idRuta = ruta.idRuta

    def consultarRuta(self):
        return self.ruta

    def asignarOperador(self, operador):
        self.operador = operador
        if operador is None:
            self.idOperador = None
        else:
            self.idOperador = operador.idOperador

    def calcularTiempoRuta(self):
        if self.ruta is None:
            return 0.0
        else:
            return self.ruta.calcularTiempoTotal()
