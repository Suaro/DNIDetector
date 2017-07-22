## Detector de DNIs y reconocimiento de caracteres OCR

A continuación se detalla el modo de uso del programa, configuraciones y diferentes diagramas de uso explicativos.

### Sobre el software

Este software fue creado para hallar un método que sirviera como alternativa eficiente a los métodos de detección de objetos tradicionales, ya que habitualmente pueden llegar a ser algo lentos. Se utiliza este algoritmo sobre DNIs para ver su funcionamiento y aprovechar su funcionalidad detectando un DNI en cualquier imagen digitalizada. 

Este software fue realizado como __Trabajo Fin de Grado__ en la __Universidad Rey Juan Carlos__.

### Requisitos

Para la ejecución del programa es necesario:


- Tener instalado [Python 2.7](https://www.python.org/downloads/)
- Tener instalado [Tesseract OCR-Engine](https://github.com/tesseract-ocr/tesseract/wiki)
- Tener instalado OpenCV 3.0.0 o superior
- Tener instaladas librerías propias de python *(se instalan con **pip install -U** seguido del nombre de la librería)* como puede ser numpy, matplotlib, imutils y cPickle.
- Sistema operativo que soporte las anteriores tecnologías.

#### Instalar OpenCV

Para instalar OpenCV, se recomienda:

1. Instalar [Anaconda](https://www.continuum.io/downloads)
2. A continuación escribir en shell
```sh
$~ anaconda search opencv
```
3. Esto último te mostrará un listado de imágenes no oficiales de OpenCV que tiene Anaconda. Elegir uno que sea compatible con vuestro sistema operativo y escribir:
```sh
$~ conda install -c NombreRepositorio NombreArchivo
```

	Por ejemplo:

	```sh
	$~ conda install -c menpo opencv3
	```

#### Ejecución del programa

Lo primero, es necesario tener descargado el proyecto, para ello habrá que hacer desde la consola de comandos

```sh
$~ git clone NombreRepositorio
```

Posteriormente, dirigirse a la carpeta DetectDNI y ejecutar el programa:

```sh
$~ cd {path}/DetectDNI
$~ {path}/DetectDNI python DetectDNI.py --images ruta/imagenes --type tipo_dni
```

##### Explicación de los parámetros

En este apartado se detalla cuales son los argumentos que recibe el programa:

- __--images__ <span style="color:green">__(Opcional)__</span> : Este argumento recibe la ruta de la imagen o la carpeta de imágenes en las que se va a detectar si hay un DNI.

- __--front__ <span style="color:green">__(Opcional)__</span> : Este argumento recibe la ruta de la imagen perteneciente a la cara frontal del DNI.

- __--back__ <span style="color:green">__(Opcional)__</span> : Este argumento recibe la ruta de la imagen perteneciente a la cara trasera del DNI.

- __--type__ <span style="color:red">__(Obligatorio)__</span> : Este argumento determina el tipo de DNI que se quiere detectar en la imagen. Puede ser _old_, _old_back_, _new_, _new_back_.

- __--mode__ <span style="color:green">__(Opcional)__</span>: Este argumento determina el modo de ejecución del programa, puede ser _recognition_ o _detect_

##### Tipos de ejecución del programa

A continuación se detallan las funcionalidades que tiene el software

###### Detección de DNI en carpeta de imágenes

El software puede leer de manera iterativa las imágenes de una carpeta (o la ruta de una imagen individual) de manera que detectará en todas ellas si hay un DNI y en que posición. Por otro lado, extraerá toda la información del mismo si se especifica el modo _recognition_ o se mostrará la detección mediante _detect_

```sh
$~ {path}/DetectDNI python DetectDNI.py --images ruta/imagenes --type tipo_dni --mode mode
```

###### Detección de DNI por ambas caras

El software también se puede utilizar para extraer la información de un DNI pasándole una foto de ambas caras del mismo, detectaría y extraería la información de ambos. En este caso, también se hará un proceso de validación para comprobar que la mayoría de la información extraída ha sido correctamente leída y de este modo, avisar si fuese necesario hacer una nueva foto del DNI.

```sh
$~ {path}/DetectDNI python DetectDNI.py --front /ruta/DNI/frontal --back /ruta/DNI/trasera --type tipo_dni --mode mode
```


##### Tipos de DNI

El programa está preparado para leer dos tipos de DNI tanto por delante como por detrás. 

El primero, tipo **old** para la parte frontal y **old_back** para la trasera, sería de este tipo:

![DNI](https://www.securitynull.net/files/dni_7.jpg)


El segundo, tipo **new** para la parte frontal y **new_back** para la trasera, sería de este tipo:

![DNI](http://static01.heraldo.es/uploads/imagenes/8col/2015/08/28/_imagendni_b3c3dc6a.jpg?88000fd276d719adfd01cda13ba31335)


### Configuración

La carpeta config contiene los diferentes parámetros de configuración del programa, en ellos se incluye:

- Puntos de interés de cada canal de la imagen RGB modelo.
- Descriptores de cada canal de la imagen RGB modelo.
- Configuración de los parámetros que indican las posiciones de la información a extraer en la imagen modelo.

### Información

**Titulo** :  Detector de DNIs y reconocimiento de caracteres OCR
**Autor** : Adrián Suárez (Suaro)
**Email** : adrian9521@hotmail.com
**Última actualización**:   21 de Mayo de 2017






