# Proyecto final. Un proceso de ingeniería de características
## Curso Ingeniería de Características

La finalidad de este proyecto es realizar una comparación del pronóstico meteorológico realizado en la Universidad de Sonora mediante el proyecto PROMETEUS y el pronóstico que ofrece la NASA mediante el proyecto EARTHDATA. Para las pruebas utilizaremos el aeropuerto de Hermosillo como punto de revisión. 
PROMETEUS genera diariamente datos de pronóstico del noroeste del México, con una resolución de 5.4 y 1.8 Km.
EARTHDATA genera la información con un atraso de 4 meses aproximadamente, el algoritmo IMERG maneja una resolución de 10 Km.

### Obtención de los datos
Las fuentes de datos son EARTHDATA y PROMETEUS, en este proceso se descargarán los datos utilizando la metodología especificada por el emisor de la información. Por lo general vienen en formato RAW y es por eso que es necesario pre-procesarlos para despues trabajar con ellos.  
El procedimiento que se siguió para su descarga fue el siguiente [Obtención de Datos](obtencion_datos.md)

### Generación de datos tidy
Para este proceso se utilizo código en python mediante una libreta de jupyter, también se genero como script. Los archivos se llaman [generador_datos_tidy](codigo/generador_datos_tidy.ipynb) y [generador_datos_tidy.py](codigo/generador_datos_tidy.py)  
El proceso que se siguio fue tomar cada uno de los datos de PROMETEUS y la NASA para extraer de cada uno las características de 3 ciudades de Hermosillo, las cuales se eligieron porque son las que estaban en todos los dataset de PROMETEUS. Se hizo lo mismo para los datos de la NASA, primero buscando las coordenadas que mas se acercaban a las coordenadas a comparar, luego de ahi se extrajo la información de solo esos puntos. Por ultmo se genero un solo dataframe que se guardo en el archivo [datos_tidy](datos_tidy.csv) y el diccionario de datos [diccionario_datos](diccionario_datos.csv)

### Limpieza de datos
Se trabajó en la correcta codificación de datos de tipo fecha, numericos y de cadenas, asi como la armonización de variables. También se le realizaron técnicas para encontrar y solucionar el problema de datos faltantes que si fueron bastantes mas de los esperados, una de las tecnicas para la imputación de los datos fue interpolar los valores de precipitacion con el ultimo valido y el siguiente valido al faltante. En el caso de los nombres de ciudad solo se asignaron la que les correspondia. Por último se genero otro dataset en csv con la información limpia y completa.
El código que se utilizó fue el siguiente. 
  


