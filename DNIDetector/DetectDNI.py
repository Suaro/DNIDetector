import numpy as np
import imutils
from imutils import paths
import cv2
from matplotlib import pyplot as plt
from DNIUtils import DNIUtils
from DNIValidator import DNIValidator
from DNIDetector import DNIDetector
from DNILocalizator import DNILocalizator
from DNIRecognizer import DNIRecognizer
import argparse
from DNIConfiguration import DNIConfiguration
import os
import sys


class DetectDNI:
    def __init__(self):
        return;


    @staticmethod
    def detect_dni(image_path, config, mode):
        """
        Este metodo recibe una imagen y detecta si hay un DNI en ella.
        :param image_path: Ubicacion de la imagen (ruta relativa o absoluta)
        :param config: Tipo de configuracion del DNI (old, old_back, new, new_back)
        :param mode: Modo de ejecucion del programa
        :return: Region detectada.
        """
        # Leemos la imagen
        img = cv2.imread(image_path)  # trainImage
        # Obtenemos su ancho y alto por si hubiera que redimensionar
        height, width = img.shape[:2]

        if height > width:
            img = imutils.resize(img, height=1200)
        else:
            img = imutils.resize(img, width=1200)

        # Obtenemos el nuevo ancho y alto
        height, width = img.shape[:2]

        # Aplicamos ORB y FLANN a los canaless
        detector = DNIDetector(config, img)
        matches_array = detector.search_keypoints_and_matches()

        print("\nLISTO!")

        angles, borders_train = DetectDNI.get_border_and_angles(img, config, height, width, matches_array)
        validator = DNIValidator()

        # Validamos si la region cumple las condiciones para contener un DNI
        accepted_region = validator.validate_region(borders_train)


        if accepted_region:

            #Si el modo era deteccion, dibujamos la zona detectada
            if mode == "detect":
                # Pintamos el rectangulo
                img = DetectDNI.draw_region(img,borders_train)
            else:
                # Rotamos la imagen en base a su angulo medio y leemos su informacion
                angle_median = np.median(angles)
                img = utils.rotate_and_crop(img, angle_median, height, width, borders_train)

        return img




    @staticmethod
    def get_border_and_angles(img, config, height, width, matches_array):
        """
        Metodo que obtiene los angulos y esquinas del DNI.
        :param img: Imagen de entrenamiento
        :param config: Objeto que contiene la configuracion.
        :param height: Alto de la imagen de entrenamiento.
        :param width: Ancho de la imagen de entrenamiento.
        :param matches_array: Array que contiene las coincidencias.
        :return: 
        """

        borders_query = [(-40, 0), (config.width + 10, 0), (config.width + 10, config.height), (-40, config.height)]
        borders_train = []
        angles = []
        for border in borders_query:
            # Buscamos la esquina correspondiente de la imagen modelo en la imagen de entrenamiento.
            localizator = DNILocalizator(width, height, border[0], border[1], img)
            arraypoints = localizator.search_point(matches_array)

            # Obtenemos la mediana de los valores de los arrays
            angle_median, distance_height, distance_width, x_median, y_median = utils.get_median_values(arraypoints,
                                                                                                        config.height,
                                                                                                        config.width)
            if x_median > width:
                x_median = width
            if y_median > height:
                y_median = height

            angles.append(angle_median)

            borders_train.append((x_median, y_median, angle_median, distance_height, distance_width))
        return angles, borders_train





    @staticmethod
    def draw_region(img, borders_train):
        """
        Metodo que dibuja la region en la que se ubica el DNI
        :param img: Imagen original
        :param borders_train: Esquinas de la region
        :return: 
        """
        i = 0
        finish = False

        while not finish:
            border_1 = borders_train[i]
            if i + 1 >= len(borders_train):
                i = -1
                finish = True
            border_2 = borders_train[i + 1]
            img = cv2.line(img, (int(border_1[0]), int(border_1[1])), (int(border_2[0]), int(border_2[1])),
                           (0, 0, 255), 15)
            i = i + 1
        return img




    @staticmethod
    def extract_info_dni(config, img, type):
        """
        Metodo que extrae toda la informacion del DNI y la imprime por pantalla.
        :param config: Configuracion del DNI
        :param img: Imagen que contiene el DNI
        :param type: Tipo de DNI que se va a evaluar
        """
        recog = DNIRecognizer(config, img, type)
        text = recog.extract_all_info()
        print(text)




    @staticmethod
    def extract_front_validation_info(config, img, type):
        """
        Metodo que extrae la informacion necesaria de la cara frontal para validar el reconocimiento del DNI
        :param config: Configuracion del DNI
        :param img: Imagen que contiene el DNI
        :param type: Tipo de DNI que se va a evaluar
        """
        recog = DNIRecognizer(config, img, type)
        name = recog.get_text(recog.get_dni_name())
        subname1 = recog.get_text(recog.get_dni_subname1())
        subname2 = recog.get_text(recog.get_dni_subname2())
        num = recog.get_text(recog.get_dni_num())[:8]

        return [name, subname1, subname2, num]



    @staticmethod
    def extract_back_validation_info(config, img, type):
        """
        Metodo que extrae la informacion necesaria de la cara trasera para validar el reconocimiento del DNI
        :param config: Configuracion del DNI
        :param img: Imagen que contiene el DNI
        :param type: Tipo de DNI que se va a evaluar
        """
        recog = DNIRecognizer(config, img, type)
        mrz = recog.get_text(recog.get_mrz())

        return mrz



    ################# PROGRAMA PRINCIPAL #################


    @staticmethod
    def evalue_type(type):
        types_allowed = ["old","old_back","new","new_back"]
        if not type in types_allowed:
            sys.tracebacklimit = 0
            raise ValueError(ERROR_TYPE)



if __name__ == '__main__':

    ERROR_ARGUMENTS = "Entry parameters are incorrect\n\nThe possibilities are:\n * python DetectDNI.py --images IMAGES_PATH --type TYPE \n * python DetectDNI.py --front FRONT_IMAGE_PATH --back BACK_IMAGE_PATH --type TYPE\n "
    ERROR_FRONT_BACK = "--front and --back arguments must be images."
    ERROR_IMAGE_RECOGNITION = "Images Require better quality to be recognized."
    ERROR_MODE = "Unrecognized mode. Available modes are: 'detect' or 'recognition'"
    ERROR_TYPE = "Unrecognized types. Types allowed are: 'old', 'old_back', 'new' or 'new_back'"

    # Declaramos variables del programa principal
    arg = argparse.ArgumentParser()
    arg.add_argument("--front", required=False, help="path to image of DNI front")
    arg.add_argument("--back", required=False, help="path to image of DNI back")
    arg.add_argument("--images", required=False, help="path to images directory")
    arg.add_argument("--type", required=True, help="type of dni, could be: old, old_back, new, new_back")
    arg.add_argument("--mode", required=False, default = "detect", help="Mode of program execution. Could be: detect or recognition")
    args = vars(arg.parse_args())

    type = args["type"]
    DetectDNI.evalue_type(type)
    utils = DNIUtils()

    #Si recibimos tanto el argumento de la imagen frontal como el de la imagen trasera...
    if args["back"] and args["front"]:

        #Si ambos son un archivo...
        if os.path.isfile(args["back"]) and os.path.isfile(args["front"]):

            #Configuramos y detectamos ambas imagenes
            config_front = DNIConfiguration(type)
            type_back = type + "_back"
            config_back = DNIConfiguration(type_back)
            img_front = DetectDNI.detect_dni(args["front"], config_front, args["mode"])
            img_back = DetectDNI.detect_dni(args["back"], config_back, args["mode"])

            #Si el modo de ejecucion es reconocimiento, validamos y extraemos la informacion si es posible
            if args["mode"] == "recognition":
                validator = DNIValidator()
                info_front = DetectDNI.extract_front_validation_info(config_front, img_front, type)
                info_back = DetectDNI.extract_back_validation_info(config_back, img_back, type_back)
                accepted = validator.validate_recognition(info_front, info_back)

                #Si la region es detectada...
                if accepted:
                    DetectDNI.extract_info_dni(config_front, img_front, type)
                    DetectDNI.extract_info_dni(config_back, img_back, type_back)
                else:
                    sys.tracebacklimit = 0
                    raise ValueError(ERROR_IMAGE_RECOGNITION)

            #Si el modo es otro, se devolvera la imagen detectada.
            elif args["mode"] == "detect":
                plt.imshow(img_front, ), plt.show()
                plt.imshow(img_back, ), plt.show()
            else:
                sys.tracebacklimit = 0
                raise ValueError(ERROR_MODE)

        #Si uno de los dos parametros no es un archivo, devolvemos error.
        else:
            sys.tracebacklimit = 0
            raise ValueError(ERROR_FRONT_BACK)

    #Si el argumento es una imagen o una carpeta de imagenes
    elif args["images"]:
        # Inicializamos la configuracion en base al modo
        config = DNIConfiguration(type)
        x = 0

        # Para todas las imagenes del directorio recogido en --images

        if os.path.isdir(args["images"]):
            for imagePath in paths.list_images(args["images"]):
                print(imagePath)

                img = DetectDNI.detect_dni(imagePath, config, args["mode"])

                if args["mode"] == "recognition":
                    DetectDNI.extract_info_dni(config, img, type)
                elif args["mode"] == "detect":
                    plt.imshow(img, ), plt.show()
                else:
                    sys.tracebacklimit = 0
                    raise ValueError(ERROR_MODE)


                x = x + 1

        #Si fuera una sola imagen
        else:
            img = DetectDNI.detect_dni(args["images"], config, args["mode"])

            if args["mode"] == "recognition":
                DetectDNI.extract_info_dni(config, img, type)
            elif args["mode"] == "detect":
                plt.imshow(img, ), plt.show()
            else:
                sys.tracebacklimit = 0
                raise ValueError(ERROR_MODE)
    else:
        sys.tracebacklimit = 0
        raise Exception(ERROR_ARGUMENTS)
