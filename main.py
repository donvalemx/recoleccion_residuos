
import webview
from controlador import ControladorRecoleccion

if __name__ == "__main__":
    
 controlador = ControladorRecoleccion()
 
 webview.create_window(
        "Simulador de Recolección de Residuos",
        "vista/index.html",
        js_api=controlador,
        width=1400, 
        height=900, 
        
        resizable=True,
    )
 webview.start()

