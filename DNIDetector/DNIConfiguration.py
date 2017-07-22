import numpy as np
import cPickle
import cv2


class DNIConfiguration:


    #Constructor



    def __init__(self,type):
        """
        Constructor de la clase DNIConfiguration, que en base al modo proporcionado, inicializa
        la configuracion necesaria para del DNI de entrenamiento

        :param type -- Tipo de dni
        """

        #Obtenemos el fichero de configuracion y la ruta de los archivos de configuracion
        path_config, config_file = self.get_path(type)
        path = path_config + config_file

        #Leemos el contenido del fichero
        with open(path) as f:
            content = f.readlines()

        content = [x.strip() for x in content]
        self.width = float(content[0].split(';')[1])
        self.height = float(content[1].split(';')[1])

        #Configuramos en base al modo
        if type == "old" or type == "new":
            self.configurate_front(content)
        elif type == "old_back" or type == "new_back":
            self.configurate_back(content,path)

        self.initialize_keypoints_and_descriptors(path_config)



    # Methods


    @staticmethod
    def get_path(type):
        """
        Metodo que configura el path en base al modo proporcionado

        :param type -- Tipo de dni
        :return path_config -- Directorio de la configuracion
        :return config_file -- Archivo de configuracion
        """

        # Comprobamos el modo de DNI que se quiere evaluar

        if type == "old":  # DNI front blue
            path_config = "config/old/"
            config_file = "old_config.txt"
        elif type == "old_back":  # DNI back blue
            path_config = "config/old_back/"
            config_file = "old_back_config.txt"
        elif type == "new":  # DNI front new
            path_config = "config/new/"
            config_file = "new_config.txt"
        elif type == "new_back":  # DNI back new
            path_config = "config/new_back/"
            config_file = "new_back_config.txt"

        return path_config, config_file




    def initialize_keypoints_and_descriptors(self,path_config):
        """
        Metodo que inicializa los keypoints y descriptores de la imagen modelo

        :param path_config -- Directorio de la configuracion
        """
        self.b_kp = self.read_keypoints(path_config,"b_kp.txt")
        self.g_kp = self.read_keypoints(path_config, "g_kp.txt")
        self.r_kp = self.read_keypoints(path_config, "r_kp.txt")
        self.b_des = self.read_descriptors(path_config, "b_des.txt")
        self.g_des = self.read_descriptors(path_config, "g_des.txt")
        self.r_des = self.read_descriptors(path_config, "r_des.txt")


    @staticmethod
    def read_keypoints(path_config, config_file):
        """
        Metodo que lee los keypoints de un fichero y los convierte en un array de keypoints

        :param path_config -- Directorio de la configuracion
        :param config_file -- Archivo de configuracion
        :return kp -- Keypoints del archivo
        """

        path = path_config + config_file
        index = cPickle.loads(open(path).read())
        kp = []
        for point in index:
            temp = cv2.KeyPoint(x=point[0][0], y=point[0][1], _size=point[1], _angle=point[2], _response=point[3],
                                _octave=point[4], _class_id=point[5])
            kp.append(temp)

        return kp


    @staticmethod
    def read_descriptors(path_config, config_file):
        """
        Metodo que lee los descriptores de un fichero y los convierte en un numpy array de descriptores
        :param path_config -- Directorio de la configuracion
        :param config_file -- Archivo de configuracion
        :return descriptors -- Descriptores del archivo
        """
        path = path_config + config_file
        index = cPickle.loads(open(path).read())
        descriptors = []
        for i in xrange(len(index)):
            temp = index[i] * 1
            descriptors.append(temp)
        descriptors = np.asarray(descriptors)
        return descriptors






    def configurate_front(self,content):
        """
        Metodo que configura la parte frontal del dni en base a su archivo de configuracion

        :param content -- Contenido del fichero de configuracion
        """
        self.type = "front"
        self.name = eval(content[2].split(';')[1])
        self.subname2 = eval(content[3].split(';')[1])
        self.subname1 = eval(content[4].split(';')[1])

        self.gender = eval(content[5].split(';')[1])
        self.nationality = eval(content[6].split(';')[1])

        self.birthday = eval(content[7].split(';')[1])
        self.photo = eval(content[8].split(';')[1])
        self.idesp = eval(content[9].split(';')[1])

        self.validity = eval(content[10].split(';')[1])
        self.signature = eval(content[11].split(';')[1])
        self.num = eval(content[12].split(';')[1])





    def configurate_back(self, content, path):
        """
        Metodo que configura la parte trasera del dni en base a su archivo de configuracion

        :param content -- Contenido del fichero de configuracion
        """
        self.type = "back"
        self.placeofbirth = eval(content[2].split(';')[1])
        self.parents = eval(content[3].split(';')[1])

        self.residency = eval(content[4].split(';')[1])
        self.team = eval(content[5].split(';')[1])
        self.mrz = eval(content[6].split(';')[1])

        if path == "config/old_back/old_back_config.txt":
            self.country = eval(content[7].split(';')[1])
            self.placeofresidency = eval(content[8].split(';')[1])
            self.country2 = eval(content[9].split(';')[1])

