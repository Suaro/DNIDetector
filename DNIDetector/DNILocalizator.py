import numpy as np
from DNIUtils import DNIUtils
import math
import cv2

################  VARIABLES GLOBALES ############################

DIVISOR = 100


class DNILocalizator:




    def __init__(self, width, height,x,y,img):
        """
        Constructor de la clase DNILocalizator
        :param self -- Instancia de las variables de la clase
        :param width -- Ancho de la imagen en la que se va a asignar el punto
        :param height -- Alto de la imagen en el que se va a asignar el punto
        :param x -- punto x de la ubicacion buscada
        :param y -- punto y de la ubicacion buscada
        """
        #TODO: QUITAR ESTA IMAGEN
        self.img = img
        self.width = width
        self.height = height
        self.x = x
        self.y = y






    def search_point(self,info_array):

        """
        Metodo que busca el punto definido en el constructor de la clase en base al array de coincidencias y
        keypoints proporcionados.

        :param info_array -- Array que contiene las coincidencias y los keypoints de cada canal, separado en tuplas.
        :return arraypoints -- Array de las mejores ubicaciones del punto buscado, junto con su angulo de diferencia
                y su aspect ratio
        """

        utils = DNIUtils()
        i = 0
        arraypoints = []

        #Examinamos todos los elementos del array y hayamos los puntos en perspectiva
        while i < len(info_array):
            matches,kp1,kp2 = info_array[i]
            arraypoints.append(self.get_perspective_points(matches,kp1,kp2))
            i = i + 1

        list_arraypoints = ()
        row_length = self.width / DIVISOR
        i = 0
        #Obtenemos los maximos valores de los arraypoints obtenidos anteriormente y concatenamos
        while i < len(arraypoints):
            list_arraypoints = utils.get_max_values(arraypoints[i], list_arraypoints, row_length)
            i = i + 1

        arraypoints = np.concatenate(list_arraypoints, axis=0)


        return arraypoints






    def assign_point(self,x, y, angle_dif, size_dif):
        """
        Metodo que clasifica un punto dado en el array y posteriormente lo asigna a la posicion
        corrrespondiente junto con el angulo correspondiente a ese punto dado

        :param self -- Instancia de las variables de la clase
        :param x -- Coordenada x del punto que se va a asignar
        :param y -- Coordenada y del punto que se va a asignar
        :param angle_dif -- Angulo de diferencia entre el punto de entrenamiento y el punto modelo
        :param size_dif -- Escala del tamanno del punto de entrenamiento respecto al punto modelo

        """
        # variables locales
        utils = DNIUtils()
        result = utils.classificate_value(x, self.width, self.width / DIVISOR)
        result2 = utils.classificate_value(y, self.height, self.height / DIVISOR)
        info_point = [x, y, angle_dif, size_dif]
        # Asignamos indice
        index = (result2 * ((self.width / DIVISOR) - 1 )) + result
        # Asignamos el nuevo array creado al indice obtenido
        aux = self.arraypoints[index]
        aux.append(info_point)
        self.arraypoints[index] = aux






    def get_perspective_points(self, matches,kp1,kp2):

        """
        Metodo que mediante los keypoints y matches dados, ubica en la	imagen la esquina del DNI si este existe, mediante la obtencion del vector equivalente al vector generado en la imagen modelo

        :param matches -- coincidencias entre la imagen de entrenamiento y la imagen modelo
        :param kp1 -- Puntos de interes de la imagen modelo
        :param kp2 -- Puntos de interes de la imagen de entrenamiento
        :return arraypoints -- Array de las mejores ubicaciones del punto buscado, junto con su angulo de diferencia
                y su aspect ratio
        """

        self.initialize_arraypoints()
        i = 0

        # Mientras haya matches...
        while i < len(matches):

            # Obtenemos coordenadas x e y de los puntos de las coincidencias
            img_idx = matches[i].queryIdx
            img2_idx = matches[i].trainIdx
            (x, y) = kp1[img_idx].pt
            (x2, y2) = kp2[img2_idx].pt

            # Obtenemos sus respectivos angulos y tamanos
            size1 = kp1[img_idx].size
            size2 = kp2[img2_idx].size
            angle1 = kp1[img_idx].angle
            angle2 = kp2[img2_idx].angle
           # Obtenemos la diferencia en radianes de sus angulos, el escalado en base al tamano de ambos, el vector de la imagen1 y el arcotangente
            angle_dif = math.radians(angle2) - math.radians(angle1)
            size_dif = size2 / size1
            (vectorx, vectory) = (self.x - x, self.y - y)
            atan = math.atan2(vectory, vectorx)

            # Realizamos la correccion de angulos y obtenemos los puntos X e Y de la imagen 2, que sera la esquina buscada
            angle_correction = atan + angle_dif
            distance = math.hypot(vectorx, vectory) * size_dif
            point_x = x2 + (distance * math.cos(angle_correction))
            point_y = y2 + (distance * math.sin(angle_correction))

            # Si los puntos se han salido fuera, los metemos en el limite de la imagen
            if point_x >= self.width:
                point_x = self.width
            if point_y >= self.height:
                point_y = self.height
            if point_x < 0:
                point_x = 0
            if point_y < 0:
                point_y = 0

            self.assign_point(point_x, point_y, angle_dif, size_dif)

            i = i + 1
        return self.arraypoints






    def initialize_arraypoints(self):
        """
        Metodo que inicializa el array donde se guardaran las mejores ubicaciones, diferencia de angulo y aspect ratio
        """

        factor = (self.width / DIVISOR) * (self.height / DIVISOR)
        self.arraypoints = np.empty((factor,), dtype=object)
        i = 0
        # Inicializamos array con arrays vacios para cada fragmento de la imagen
        while i < factor:
            self.arraypoints[i] = []
            i = i + 1






