# Octoneer – Vehículo Autónomo del Equipo Octobots

**Octoneer** es un robot autónomo desarrollado por el **Equipo Octobots** para el reto **World Robot Olympiad (WRO) México Future Engineers 2025**.

Este proyecto se enfoca en construir un vehículo autónomo modular de alto rendimiento utilizando:

- 🧠 **Raspberry Pi 5 (16GB)** como unidad de procesamiento principal
- 🎥 **Cámara de Profundidad Studica** para percepción y conciencia espacial
- ⚙️ Un sistema de control personalizado con ajuste PID, lógica de estacionamiento y planificación dinámica de rutas
- 🧩 Arquitectura modular (visión, control, estacionamiento, navegación)
- 📦 Sistema basado en Python
- 📝 Documentación limpia y flujo de trabajo basado en Git para trabajo en equipo y mantenibilidad

> Nuestro objetivo es competir a nivel nacional y clasificar para el **WRO Internacional 2026 en Singapur**.

Desarrollado con ❤️ y cafeína por:
- Haziel Campos – Desarrollador principal, sistemas de percepción y control
- Equipo Octobots – Diseño mecánico, estrategia e integración

📁 Este repositorio incluye:
- Código fuente para percepción, control y navegación
- Referencias de CAD y diagramas de hardware
- Modelos entrenados y datos de prueba
- Documentación e informe técnico (en `/docs`)

> Si te gusta este proyecto, ¡únete a nuestro Discord para aumentar la comunidad de robótica y recibir retroalimentación! [Únete al Discord aquí! 🦑](https://discord.gg/gCf6xwBBVd)

> Visita nuestros post en la wiki para ver mas informacion sobre el robot

## Estructura del proyecto

> `src` carpeta principal del proyecto
<br>
`src/main.py` archivo principal donde se ejecuta toda la logica del robot  
<br>
`src/detection_functions.py` se encarga de detectar las lineas, son la funcion de deteccion de curvas
<br>
`src/Logger.py` se encarga de manejar los logs
<br> 
`src/handler/PID.py` funcion PID para la correccion de error de los sensores de distancia
<br>
`src/enums/enums.py` archivo con enums para tener el codigo limpio y no hardcodear las variables
<br>
`src/Rasp/GPIO.py` Una implementacion de RPi.GPIO usando LGPIO ya que RPi.GPIO aun no esta del todo actualizada para Raspberry Pi 5
<br>
`src/components/` Todos los actuadores y sensores del robot separados en archivos y clases para mejor legibilidad y escalabilidad
<br>
`src/clasifier.py` se encarga de detectar los obstaculos usando mascaras LAB
<br>
`src/masks.py` Los codigos LAB para las mascaras de color opencv
<br>
`/test` todos los test para probar los componentes del robot por separad