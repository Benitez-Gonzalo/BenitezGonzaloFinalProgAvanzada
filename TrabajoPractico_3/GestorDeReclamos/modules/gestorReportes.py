
from modules.clasesAbstractas import ReporteAbstracto

class GestorReportes:
    def __init__(self,repoPDF:ReporteAbstracto,repoHTML:ReporteAbstracto):
        self.__repoPDF = repoPDF
        self.__repoHTML = repoHTML
        
    def generarReportes(self,ruta_archivoPDF,ruta_archivoHTML,ruta_img):
        return self.__repoPDF.generarArchivo(ruta_archivoPDF,ruta_img),self.__repoHTML.generarArchivo(ruta_archivoHTML,ruta_img)
        
        