# Proyecto final. Un proceso de ingeniería de características
## Curso Ingeniería de Características

La finalidad de este proyecto es realizar una comparación del pronóstico meteorológico realizado en la Universidad de Sonora mediante el proyecto PROMETEUS y el pronóstico que ofrece la NASA mediante el proyecto EARTHDATA. Para las pruebas utilizaremos el aeropuerto de Hermosillo como punto de revisión. 
PROMETEUS genera diariamente datos de pronóstico del noroeste del México, con una resolución de 5.4 y 1.8 Km.
EARTHDATA genera la información con un atraso de 4 meses aproximadamente, el algoritmo IMERG maneja una resolución de 10 Km.

### Obtención de los datos
PROMETEUS
  Los datos de pronóstico de prometeus no estan disponibles públicamente, para conseguirlos es necesario escribirle al responsable del proyecto Dr. Carlos Minjares. La información completa esta en la página oficial prometeus.unison.mx.
  La información nos la proporcionaron en formato csv el cual contiene el pronóstico a 84 horas de distintas ciudades de los estados de Sonora, Sinaloa y Chihuahua.

EARTHDATA
  Para descargar los datos IMERG es necesario registrarse en https://urs.earthdata.nasa.gov/. 
  Una vez creada la cuenta vamos al siguiente enlace https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGDF_06/summary
  En la opción de "Get Data" podremos generar un archivo de texto con los archivos que deseamos descargar, mas adelante usaremos ese archivo para descargar los datasets. Los datos son multidimensionales en formato netCDF4.

  Codigo bash
  
### Análisis exploratorio de datos


### Generación del conjunto de datos tidy
  Un script de R de limpieza básica que leea los datos crudos y devuelva los datos acomodados
  Los datos en forma tidy, ya sea en csv, parquet, o sqlite
  Un diccionario de datos especificando las descripciones de cada atributo y sus unidades
### Limpieza de datos
  Armonizacion de variables
  Manejo correcto y codificacion de datos cuantitativos
  Manejo de valores perdidos
  Deteccion y manejo de valores anómalos
### Visualiacion de la información utilizando un método de reducción de características (PCA, t-SNE)

  


