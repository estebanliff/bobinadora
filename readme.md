## Como crear la imagen de raspberry

Descargar el Raspberry Pi Imager de [aca](https://www.raspberrypi.com/software/)

Conectar la memoria SD y seguir las instrucciones para instalar Raspberry Pi OS

## Para instalar el proyecto primero hay que clonar el repositorio.

1. Abrir una consola
2. Ejecutar `cd Desktop`
3. Ejecutar `git clone https://github.com/estebanliff/bobinadora.git`
4. Ejecutar `cd bobinadora`
5. Ejecutar `./install.sh`

### El script de instalacion va a crear dos archivos en el escritorio.

    start_bobinadora.sh -> Inicia el programa
    update_bobinadora.sh -> Actualiza el repositorio (debe estar cerrado el programa para actualizar)

### En la carpeta cfg se encuentran todas las configuraciones del proyecto:

cfg\presets.txt -> Tiene los textos de los botones de acceso rapido, los dos primeros los muestra en la fila superior y el resto abajo

cfg\tiempos.txt -> 

    tiempo_subida_velocidad     -> Tiempo que demora en pasar de velocidad baja a alta en segundos
    pulso_parada_rapida         -> Tiempo del pulso de parada rapida
    vueltas_para_velocidad_baja -> Cantidad de vueltas antes de terminar que pasa a baja velocidad

### En la carpeta Gabinete se encuentras los STL para imprimir el gabinete con todas sus partes
