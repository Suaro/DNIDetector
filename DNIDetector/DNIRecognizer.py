import numpy as np
import cv2
from subprocess import call
import os

class DNIRecognizer:



    def __init__(self,config,img,type):
        """
        Constructor de la clase DNIRecognizer que inicia los parametros de configuracion en base al modo proporcionado
        :param config -- Objeto que contiene la configuracion
        :param img -- Imagen de entrenamiento en la que queremos reconocer OCR
        :param type -- Tipo de imagen que se va a reconocer
        """
        self.config = config
        self.img = img
        self.type = type
        self.matrix = []
        self.initialize_recognizer()



    def initialize_recognizer(self):
        """
        Metodo que inicializa la matriz homografra del reconocedor.
        """
        height = self.config.height
        width = self.config.width
        height2, width2 = self.img.shape[:2]
        src_pts = np.float32([[0, 0], [width, 0], [0, height], [width, height]]).reshape(-1, 1, 2)
        dst_pts = np.float32([[0, 0], [width2, 0], [0, height2], [width2, height2]]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        self.matrix = M




    def get_perspective_points(self,pts):

        """
        Metodo que obtiene los puntos homografos en base a los puntos proporcionados

        :param pts -- Puntos de los que se quiere obtener los puntos homografos
        :return pt1 -- Punto homografo superior izquierda
        :return pt2 -- Punto homografo inferior izquierda
        :return pt3 -- Punto homografo inferior derecha
        :return pt4 -- Punto homografo superior derecha
        """


        dst = cv2.perspectiveTransform(pts, self.matrix)
        dst = np.int32(dst)
        pt1 = dst[0][0]
        pt2 = dst[1][0]
        pt3 = dst[2][0]
        pt4 = dst[3][0]

        return pt1,pt2,pt3,pt4






    def get_homography_subimage(self,pts):
        """
        Metodo que obtiene la imagen homografa en base a los puntos proporcionados

        :param pts -- Puntos del rectangulo de la subimagen a extraer
        :return subimage -- Subimagen homografa
        """
        pts = np.float32(pts).reshape(-1, 1, 2)
        pt1, pt2, pt3, pt4 = self.get_perspective_points(pts)
        width_subimage = pt3[0] - pt1[0]
        height_subimage = pt3[1] - pt1[1]
        subimage = self.img[pt1[1]:pt1[1] + height_subimage, pt1[0]:pt1[0] + width_subimage].copy()
        return subimage





    def get_dni_name(self):

        """
        Metodo que obtiene el nombre  en base a los puntos obtenidos de configuracion

        :return name -- Subimagen que contiene el nombre
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old" or self.type == "new":
            pts = self.config.name
            name = self.get_homography_subimage(pts)
            return name
        else:
            raise Exception("This attribute is not available for type "+self.type)





    def get_dni_subname2(self):
        """
        Metodo que obtiene el segundo apellido  en base a los puntos obtenidos de configuracion

        :return subname2 -- Subimagen que contiene el segundo apellido
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old" or self.type == "new":
            pts = self.config.subname2
            subname2 = self.get_homography_subimage(pts)
            return subname2
        else:
            raise Exception("This attribute is not available for type " + self.type)





    def get_dni_subname1(self):
        """
        Metodo que obtiene el primer apellido  en base a los puntos obtenidos de configuracion

        :return subname1 -- Subimagen que contiene el segundo apellido
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old" or self.type == "new":
            pts = self.config.subname1
            subname1 = self.get_homography_subimage(pts)
            return subname1
        else:
            raise Exception("This attribute is not available for type " + self.type)





    def get_dni_gender(self):
        """
        Metodo que obtiene el genero que viene  en base a los puntos obtenidos de configuracion

        :return gender -- Subimagen que contiene el genero que viene en el DNI
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old" or self.type == "new":
            pts = self.config.gender
            gender = self.get_homography_subimage(pts)
            return gender
        else:
            raise Exception("This attribute is not available for type " + self.type)






    def get_dni_nationality(self):
        """
        Metodo que obtiene la nacionalidad  en base a los puntos obtenidos de configuracion

        :return nationality -- Subimagen que contiene la nacionalidad
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old" or self.type == "new":
            pts = self.config.nationality
            nationality = self.get_homography_subimage(pts)
            return nationality
        else:
            raise Exception("This attribute is not available for type " + self.type)




    def get_dni_birthday(self):
        """
        Metodo que obtiene la fecha de nacimiento  en base a los puntos obtenidos de configuracion

        :return birthday -- Subimagen que contiene la fecha de nacimiento
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old" or self.type == "new":
            pts = self.config.birthday
            birthday = self.get_homography_subimage(pts)
            return birthday
        else:
            raise Exception("This attribute is not available for type " + self.type)






    def get_dni_photo(self):
        """
        Metodo que obtiene la foto  en base a los puntos obtenidos de configuracion

        :return photo -- Subimagen que contiene la foto
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old" or self.type == "new":
            pts = self.config.photo
            photo = self.get_homography_subimage(pts)
            return photo
        else:
            raise Exception("This attribute is not available for type " + self.type)





    def get_dni_idesp(self):
        """
        Metodo que obtiene el idesp  en base a los puntos obtenidos de configuracion

        :return idesp -- Subimagen que contiene el idesp
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old" or self.type == "new":
            pts = self.config.idesp
            idesp = self.get_homography_subimage(pts)
            return idesp
        else:
            raise Exception("This attribute is not available for type " + self.type)




    def get_dni_validity(self):
        """
        Metodo que obtiene la fecha de validez  en base a los puntos obtenidos de configuracion

        :return idesp -- Subimagen que contiene la fecha de validez
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old" or self.type == "new":
            pts = self.config.validity
            validity = self.get_homography_subimage(pts)
            return validity
        else:
            raise Exception("This attribute is not available for type " + self.type)




    def get_dni_num(self):
        """
        Metodo que obtiene el numero  en base a los puntos obtenidos de configuracion

        :return num -- Subimagen que contiene el numero
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old" or self.type == "new":
            pts = self.config.num
            dni_num = self.get_homography_subimage(pts)
            return dni_num
        else:
            raise Exception("This attribute is not available for type " + self.type)





    def get_signature(self):
        """
        Metodo que obtiene la firma  en base a los puntos obtenidos de configuracion

        :return signature -- Subimagen que contiene la firma
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old" or self.type == "new":
            pts = self.config.signature
            signature = self.get_homography_subimage(pts)
            return signature
        else:
            raise Exception("This attribute is not available for type " + self.type)





    def get_placeofbirth(self):
        """
        Metodo que obtiene el lugar de nacimiento  en base a los puntos obtenidos de configuracion

        :return placeofbirth -- Subimagen que contiene el lugar de nacimiento
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old_back" or self.type == "new_back":
            pts = self.config.placeofbirth
            placeofbirth = self.get_homography_subimage(pts)
            return placeofbirth
        else:
            raise Exception("This attribute is not available for type " + self.type)





    def get_parents(self):
        """
        Metodo que obtiene el nombre de los padres en base a los puntos obtenidos de configuracion
        :return parents -- Subimagen que contiene el nombre de los padres
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old_back" or self.type == "new_back":
            pts = self.config.parents
            parents = self.get_homography_subimage(pts)
            return parents
        else:
            raise Exception("This attribute is not available for type " + self.type)




    def get_residency(self):
        """
        Metodo que obtiene el domicilio en base a los puntos obtenidos de configuracion
        :return residency -- Subimagen que contiene el domicilio
        :exception: Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old_back" or self.type == "new_back":
            pts = self.config.residency
            residency = self.get_homography_subimage(pts)
            return residency
        else:
            raise Exception("This attribute is not available for type " + self.type)





    def get_team(self):
        """
        Metodo que obtiene el equipo en base a los puntos obtenidos de configuracion
        :return team -- Subimagen que contiene el equipo
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old_back" or self.type == "new_back":
            pts = self.config.team
            team = self.get_homography_subimage(pts)
            return team
        else:
            raise Exception("This attribute is not available for type " + self.type)


    def get_mrz(self):
        """
        Metodo que obtiene el MRZ (Machine Readable Zone) a los puntos obtenidos de configuracion
        :return mrz -- Subimagen que contiene el MRZ
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old_back" or self.type == "new_back":
            pts = self.config.mrz
            mrz = self.get_homography_subimage(pts)
            return mrz
        else:
            raise Exception("This attribute is not available for type " + self.type)





    def get_placeofresidency(self):
        """
        Metodo que obtiene el lugar de residencia en base a los puntos obtenidos de configuracion

        :return placeofresidency -- Subimagen que contiene el lugar de residencia
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old_back":
            pts = self.config.placeofresidency
            placeofresidency = self.get_homography_subimage(pts)
            return placeofresidency
        else:
            raise Exception("This attribute is not available for type " + self.type)





    def get_country(self):
        """
        Metodo que obtiene el pais de nacimiento en base a los puntos obtenidos de configuracion
        :return country -- Subimagen que contiene el pais de nacimiento
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old_back":
            pts = self.config.country
            country = self.get_homography_subimage(pts)
            return country
        else:
            raise Exception("This attribute is not available for type " + self.type)





    def get_country2(self):
        """
        Metodo que obtiene el pais de nacimiento en base a los puntos obtenidos de configuracion
        :return country2 -- Subimagen que contiene el pais de nacimiento
        :exception Salta si el modo proporcionado no tiene el atributo pedido
        """
        if self.type == "old_back":
            pts = self.config.country2
            country2 = self.get_homography_subimage(pts)
            return country2
        else:
            raise Exception("This attribute is not available for type " + self.type)

    @staticmethod
    def get_text(roi):
        """
        Metodo que obtiene el texto de una imagen proporcionada aplicando un treshold

        :param roi -- Imagen de la que se quiere extraer el texto
        :return text -- Texto de la imagen
        """
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi = cv2.threshold(gray_roi, 100, 255, cv2.THRESH_BINARY)[1]
        roi_text = 'roi0.tif'
        cv2.imwrite(roi_text, roi)
        call(["tesseract","roi0.tif","out"])
        path = os.getcwd()
        file = open(os.path.join( path, "out.txt" ), "r")
        text = file.read()
        file.flush()
        file.close()

        os.remove("roi0.tif")
        os.remove("out.txt")

        return text




    def extract_all_info(self):
        """
        Metodo que obtiene toda la informacion disponible del DNI

        :return output -- conjunto de  texto de la imagen
        """

        if self.type == "old" or self.type == "new":
            output = self.extract_front_values()
        elif self.type == "old_back" or self.type == "new_back":
            output = self.extract_back_values()

        return output






    def extract_front_values(self):

        """
        Metodo que devuelve un string con toda la informacion del DNI por la parte frontal

        :return output -- info del DNI
        """
        subname1 = "Primer apellido\n"+self.get_text(self.get_dni_subname1())+ "\n"
        subname2 = "Segundo apellido\n"+ self.get_text(self.get_dni_subname2()) + "\n"
        name = "Nombre\n"+self.get_text(self.get_dni_name())+ "\n"
        gender = "Sexo\n"+self.get_text(self.get_dni_gender())+ "\n"
        nationality = "Nacionalidad\n"+self.get_text(self.get_dni_nationality())+ "\n"
        birthday = "Fecha de nacimiento\n"+self.get_text(self.get_dni_birthday())+ "\n"
        idesp = "IDESP\n"+self.get_text(self.get_dni_idesp()) + "\n"
        validity = "Validez\n"+self.get_text(self.get_dni_validity()) + "\n"
        num = "DNI NUM\n"+self.get_text(self.get_dni_num()) + "\n"


        return subname1 + subname2 + name + gender + nationality + birthday + idesp + validity + num;




    def extract_back_values(self):
        """
        Metodo que devuelve un string con toda la informacion del DNI por la parte trasera

        :return output -- info del DNI
        """
        placeofbirth = "Lugar de nacimiento\n"+ self.get_text(self.get_placeofbirth())+"\n"
        parents = "Progenitores\n" + self.get_text(self.get_parents()) + "\n"
        residency = "Domicilio\n" + self.get_text(self.get_residency()) + "\n"
        team = "Equipo\n" + self.get_text(self.get_team()) + "\n"
        mrz = "Lugar de nacimiento\n" + self.get_text(self.get_mrz()) + "\n"
        text = placeofbirth + parents + residency + team + mrz

        if self.type == "old_back":
            country = "Provincia/Pais\n" + self.get_text(self.get_country()) + "\n"
            country2 = "Provincia/Pais\n" + self.get_text(self.get_country2()) + "\n"
            placeofresidency = "Lugar de domicilio\n" + self.get_text(self.get_placeofresidency()) + "\n"
            text += country + country2 + placeofresidency

        return text;