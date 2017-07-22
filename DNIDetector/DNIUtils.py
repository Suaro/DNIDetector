import math
import numpy as np
import cv2


class DNIUtils:


    """
    Funcion que inicializa DNIUtils
    """
    def __init__(self):
       return;


    @staticmethod
    def calculate_point(x, y, distance, angle):
        """
        Subprograma que calcula un punto en base a un vector en forma polar
        y su punto de origen en coordenadas cartesianas

        :param x -- Coordenada x del punto origen
        :param y -- Coordenada y del punto origen
        :param distance -- Distancia de las coordenadas polares
        :param angle -- Angulo de las coordenadas polares
        :return pt_x -- Punto x calculado
        :return pt_y -- Punto y calculado
        """
        pt_x = x + (distance * math.cos(angle))
        pt_y = y + (distance * math.sin(angle))
        return pt_x, pt_y


    @staticmethod
    def classificate_value(value, rang, denom):
        """
        Metodo que clasifica un valor en un la franja de un rango comprendido.
        En este caso,  sirve para clasificar en que altura esta el punto x o y
        en base a la altura o anchura proporcionada

        :param value -- Valor que se quiere clasificar
        :param rang -- Valor maximo en el que se puede clasificar
        :param denom -- Tamanno de las franjas en las que se divide el valor maximo

        :return result -- indice de la franja en el que se clasifica el valor

        """


        found = False
        factor = 1
        result = 0
        while found == False:
            if value <= ((rang * factor) / denom):
                found = True
                result = factor - 1
            else:
                factor = factor + 1

        return result


    @staticmethod
    def get_max_values(arraypoints, list_arraypoints, row_length):
        """
        Metodo que obtiene el array con mayor tamanno de un array y annade a la lista tanto el valor maximo como sus ocho adyacentes

        :param    arraypoints -- Array que hay que evaluar
        :param   list_arraypoints -- Lista de valores a devolver.
        :param   row_length -- Tamanno de la fila de la imagen
        :return list_arraypoints -- Lista de valores maximos
        """

        max_value = max(arraypoints, key=lambda x: len(x))
        max_index = arraypoints.tolist().index(max_value)
        adjacents = [row_length+1, row_length, row_length-1, 1,0,-1,-row_length+1, -row_length, -row_length-1]
        i = 0
        while i < len(adjacents):
            index = max_index + adjacents[i]
            if index < len(arraypoints) and index >= 0 and len(arraypoints[index]) > 0:
                    list_arraypoints = list_arraypoints + (arraypoints[index],)
            i = i + 1


        return list_arraypoints


    @staticmethod
    def rotate_and_crop(img,angle,original_height,original_width, borders_train):
        """
        Metodo que rota una imagen y devuelve una subimagen buscada
        a partir de un punto (x,y) y su ancho y alto

        :param img -- Imagen que se va a rotar
        :param angle -- Angulo de rotacion
        :param original_height -- Alto original de la imagen
        :param original_width -- Ancho original de la imagen
        :param borders_train -- Esquinas del DNI detectado.
        :param x -- Punto x de la esquina superior izquierda de la subimagen a extraer
        :param y -- Punto y de la esquina superior izquierda de la subimagen a extraer
        :return rotated -- Imagen rotada y cortada
        """

        utils = DNIUtils()
        translate_gap_x = 0
        translate_gap_y = 0
        #Calculamos las mayores distancias del cuadrilatero para recoger el area detectada completa.
        distance_height = max(utils.calculate_distance(borders_train[0], borders_train[3]),utils.calculate_distance(borders_train[1],borders_train[2]))
        distance_width = max(utils.calculate_distance(borders_train[0], borders_train[1]),utils.calculate_distance(borders_train[2],borders_train[3]))

        #Calculamos el desfase de angulo y el de traslacion
        angle_gap = DNIUtils.calculate_angle_gap(borders_train[0][0],borders_train[0][1],borders_train[1][0],borders_train[1][1], angle, original_width,original_height)
        angle = angle + angle_gap
        rotated_x, rotated_y = DNIUtils.rotate_point(borders_train[0][0], borders_train[0][1], angle, original_width, original_height)

        if rotated_x < 0:
            translate_gap_x = -rotated_x
            rotated_x = 0

        if rotated_y < 0:
            translate_gap_y = -rotated_y
            rotated_y = 0

        #Aplicamos las transformaciones y extraemos la imagen
        rotated = DNIUtils.rotate_image(img,angle,original_width,original_height,translate_gap_x,translate_gap_y)
        rotated = rotated[rotated_y:rotated_y + distance_height, rotated_x:rotated_x + distance_width]

        return rotated


    @staticmethod
    def get_median_values(arraypoints,height,width):
        """
        Metodo que obtiene la mediana de los valores de los arrays proporcionados
        :param arraypoints: Array que contiene los arrays de puntos
        :param height: Alto de la imagen original de entrenamiento
        :param width: Ancho de la imagen original de entrenamiento
        :return: angle_median -- Mediana de los angulos del array
        :return: distance_height -- Alto de la subimagen a obtener
        :return: distance_width -- Ancho de la subimagen a obtener
        :return: x_median -- Punto x medio
        :return y_median -- Punto y medio
        """
        median = np.median(arraypoints, axis=0)
        angle_median = median[2]
        distance_height = median[3] * height
        distance_width = median[3] * width
        x_median = median[0]
        y_median = median[1]

        return angle_median,distance_height,distance_width,x_median,y_median


    @staticmethod
    def calculate_distance (pt1, pt2):
        """
        Este metodo calcula la distancia entre dos puntos
        :param pt1: Punto origen
        :param pt2: Punto destino
        :return: Distancia
        """
        return math.hypot(pt2[0]-pt1[0],pt2[1]-pt1[1])



    @staticmethod
    def rotate_point (x, y, angle, width, height):
        """
        Esta funcion rota un punto el angulo especificado
        :param x: Punto x
        :param y: Punto y
        :param angle: Angulo con el que queremos rotar nuestro punto
        :param width: Anchura original de la imagen respecto a la que vamos a rotar el punto
        :param height:  Altura original de la imagen respecto a la que vamos a rotar el punto
        :return: rotated_x -- punto x rotado
        :return: rotated_y -- punto y rotado
        """

        x_diff = x - (width / 2)
        y_diff = y - (height / 2)

        rotated_x = x_diff * math.cos(-angle) - y_diff * math.sin(-angle) + (width / 2)
        rotated_y = x_diff * math.sin(-angle) + y_diff * math.cos(-angle) + (height / 2)

        return rotated_x, rotated_y



    @staticmethod
    def rotate_image (img, angle, width, height,translate_gap_x,translate_gap_y ):
        """
        Esta funcion rota una imagen los grados especificados
        :param img: Imagen que se va a rotar
        :param angle: Angulo con el que queremos rotar la imagen en radianes
        :param width: Anchura de la imagen original
        :param height: Altura de la imagen original
        :param translate_gap_x : parametro que determina cual es el desfase en X si la imagen se ha salido del margen para corregir la traslacion
        :param translate_gap_y : parametro que determina cual es el desfase en Y si la imagen se ha salido del margen para corregir la traslacion
        :return: rotated -- Imagen rotada
        """
        first_translation = np.array(
            [[1, 0, float(width / 2.0)], [0, 1, float(height / 2.0)], [0, 0, 1]])
        second_translation = np.array(
            [[1, 0, float(-width / 2.0)+translate_gap_y], [0, 1, float(-height / 2.0)+translate_gap_x], [0, 0, 1]])
        rotation = np.array([[math.cos(-angle), -math.sin(-angle), 0], [math.sin(-angle), math.cos(-angle), 0], [0, 0, 1]])

        result = np.matmul(first_translation, rotation)
        result = np.matmul(result, second_translation)[:2]
        result = np.float32(result[:])

        rotated = cv2.warpAffine(img, result, (int(1.6 * width), int(1.6 * height)))

        return rotated

    @staticmethod
    def calculate_angle_gap(x, y, x2, y2, angle, width,height):
        """
        Metodo que calcula el posible desfase que puede existir en la imagen rotada.
        Para esto, se coge un punto que deberia estar a 90 grados una vez aplicada la rotacion,
        y se calcula la diferencia existente.
        :param x: Punto x de referencia para calcular el desfase
        :param y: Punto y de referencia para calcular el desfase
        :param x2: Punto x que deberia formar angulo de 90 grados con (x,y)
        :param y2: Punto y que deberia formar angulo de 90 grados con (x,y)
        :param angle: Angulo de rotacion original
        :param width: Ancho de la imagen original
        :param height: Alto de la imagen original
        :return: Desfase de angulo.
        """

        rotated_x, rotated_y = DNIUtils.rotate_point(x,y,angle,width,height)
        rotated_x2, rotated_y2 = DNIUtils.rotate_point(x2,y2,angle,width,height)

        (v1, v2) = (rotated_x2-rotated_x,rotated_y2-rotated_y)

        (u1, u2) = (rotated_x2-rotated_x, 0)

        angle_gap = DNIUtils.calculate_angle(u1, u2, v1, v2)

        if rotated_y2 > rotated_y:
            return angle_gap
        else:
            return -angle_gap



    @staticmethod
    def calculate_angle(u1, u2, v1, v2):
        """
        Metodo que calcula el angulo formado por dos vectores
        :param u1: Primer componente del vector U
        :param u2: Segundo componente del vector U
        :param v1: Primer componente del vector V
        :param v2: Segundo componente del vector V
        :return: Angulo que forman.
        """
        angle = math.acos(abs(u1 * v1 + u2 * v2) / (math.hypot(u1, u2) * math.hypot(v1, v2)))
        return angle
