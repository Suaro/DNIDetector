
import cv2
import numpy as np

ORB = cv2.ORB_create(nfeatures=2000)
FLANN_INDEX_KDTREE = 0
FLANN_INDEX_LSH = 6
MULTI_PROBE_LEVEL = 2
CHECKS = 50
DISTANCE_FACTOR = 0.75
TABLE_NUMBER = 12
KEY_SIZE = 20

class DNIDetector:


    def __init__(self, config, img):
        """
        Constructor de la clase DNIDetector

        :param config -- Configuracion de la imagen modelo
        :param img -- imagen de entrenamiento
        """
        self.config = config
        self.img = img





    def search_keypoints_and_matches(self):
        """
        Metodo que obtiene los keypoints de la imagen de entrenamiento y las coincidencias con los keypoints
        de la configuracion con cada uno de los tres canales de la imagen de entrenamiento proporcionada

        :param info_array -- Array que contiene las coincidencias y los keypoints de cada canal, separado en tuplas.
        """

        # Separamos en sus canales RGB
        b, g, r = cv2.split(self.img)

        #Obtenemos los keypoints de la imagen de entrenamiento y las coincidencias con
        matches,kp = self.apply_orb_and_flann(b,self.config.b_des)
        matches2, kp2 = self.apply_orb_and_flann(g, self.config.g_des)
        matches3, kp3 = self.apply_orb_and_flann(r, self.config.r_des)

        info_array = [(matches, self.config.b_kp, kp), (matches2, self.config.g_kp, kp2), (matches3, self.config.r_kp, kp3)]

        return info_array

    @staticmethod
    def apply_orb_and_flann(img, configdes):

        """
        Subprograma que obtiene las mejores coincidencias y los arrays de keypoints de las imagenes dadas, usando ORB y FLANN

        :param img -- Imagen que se va a comparar
        :param configdes -- Descriptores obtenidos de la configuracion
        :return good -- Mejores coincidencias obtenidas
        :return kp -- Keypoints de la imagen de entrenamiento
        """

        print("\nDetectando coincidencias...")

        # Buscamos keypoints y descriptores con ORB
        kp, des = ORB.detectAndCompute(img, None)

        # Creamos los parametros de FLANN
        index_params = dict(algorithm=FLANN_INDEX_LSH,
                            table_number=TABLE_NUMBER,
                            key_size=KEY_SIZE,
                            multi_probe_level=MULTI_PROBE_LEVEL)
        search_params = dict(checks=CHECKS)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        # Buscamos las coincidencias
        matches = flann.knnMatch(configdes, des, 2)

        # Devolvemos las mejores coincidencias y los keypoints
        good = []
        for m_n in matches:
            if len(m_n) != 2:
                continue
            (m, n) = m_n
            if m.distance < DISTANCE_FACTOR * n.distance:
                good.append(m)

        return good, kp