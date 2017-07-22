from DNIUtils import DNIUtils
import math

class DNIValidator:

    def __init__(self):
        return;

    @staticmethod
    def validate_region(borders):
        """
        Metodo que valida si una region puede ser un DNI en base a las esquinas que lo forman.
        :param borders: Array que contiene las esquinas de la region detectada 
        :return: True si es valida y False en caso contrario.
        """

        finish = False
        i = -2

        #Mientras queden combinaciones de dos rectas que evaluar, se evalua el angulo que forman y si es aceptado.
        while not finish:

            border_1 = borders[i]
            border_2 = borders[i + 1]
            border_3 = borders[i + 2]

            (u1, u2) = (border_1[0] - border_2[0], border_1[1] - border_2[1])
            (v1, v2) = (border_3[0] - border_2[0], border_3[1] - border_2[1])
            accepted_angle = DNIValidator.validate_angle(u1,u2,v1,v2)

            if not accepted_angle:
                finish = True
                return False

            i = i + 1

            if i + 2 >= len(borders):
                finish = True

        return True

    @staticmethod
    def validate_recognition(info_front, info_back):
        """
        Metodo que valida el reconocimiento de un DNI si la informacion recopilada de su parte frontal
        coincide mayoritariamente con la informacion recopilada de la parte trasera.
        :param info_front: Informacion extraida de la parte frontal.
        :param info_back: Informacion extraida de la parte trasera.
        :return: True si es valida y False si no lo es.
        """

        name = info_front[0].replace("\n","").replace(" ", "")
        subname1 = info_front[1].replace("\n","").replace(" ", "")
        subname2 = info_front[2].replace("\n","").replace(" ", "")
        num = info_front[3].replace("\n","").replace(" ", "")

        result = 0

        if name in info_back:
            result += 1
        if subname1 in info_back:
            result += 1
        if subname2 in info_back:
            result += 1
        if num in info_back:
            result += 1

        if result >= 2:
            return True

        return False

    @staticmethod
    def validate_angle(u1, u2, v1, v2):
        """
        Metodo que valida si el angulo pertenece a un cuadrilatero
        :param u1:
        :param u2: 
        :param v1: 
        :param v2: 
        :return: 
        """
        utils = DNIUtils()
        angle = math.degrees(abs(utils.calculate_angle(u1,u2,v1,v2)))

        if angle >= 60 and angle <= 120:
            return True
        else:
            return False

