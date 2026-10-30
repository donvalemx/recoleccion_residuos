# Sistema de Recolección de Residuos

Proyecto académico desarrollado como parte de la materia de Programación Orientada a Objetos.

La aplicación simula un sistema de recolección de residuos sobre una ciudad representada mediante una malla. Permite generar puntos de recolección para distintos tipos de residuos, calcular rutas, obtener distancia y tiempo estimado de recorrido, y generar una ruta alternativa mediante el método de vecino más cercano.

## Tecnologías utilizadas

- Python
- JavaScript
- HTML
- CSS
- pywebview

## Arquitectura

La solución utiliza el patrón Modelo-Vista-Controlador (MVC):

- `modelos.py`: contiene las clases, reglas y lógica del modelo.
- `controlador.py`: coordina la comunicación entre la vista y el modelo.
- `app.js`: contiene la lógica de interacción de la vista.
- `index.html` y `styles.css`: definen la interfaz gráfica.
- `main.py`: punto de inicio de la aplicación.

## Requisitos

Es necesario contar con Python instalado.

Las dependencias pueden instalarse mediante:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` contiene:

```text
pywebview
```

## Ejecución

Ubicarse en la carpeta principal del proyecto y ejecutar:

```bash
python main.py
```



## Propósito

Este proyecto fue desarrollado con fines académicos para aplicar conceptos de Programación Orientada a Objetos, diseño mediante MVC, manejo de excepciones e integración entre Python y tecnologías web mediante pywebview.