"""La capa de persistencia maneja el almacenamiento y recuperación de datos, por ejemplo,
usando archivos de texto. Esta capa es la que se debe modificar o reemplazar si cambio de tecnología
para almacenar los datos (por ejemplo con una base de datos). La capa de dominio no debe verse afectada
por este cambio.
"""
import os, datetime
from collections import defaultdict

def guardar_historial_web(usuario, aciertos, num_rondas):
    """Función que carga un usuario y sus aciertos
    al historial de la app web
    """
    archihistorial = open('./data/historial_web.txt','a+', encoding="utf-8")
    dt = datetime.datetime.today()
    archihistorial.write(str(usuario) + ',' +  str(aciertos) + "," + str(num_rondas) + ','+ 
                         str(dt.strftime('%d/%m/%Y')) + '\n')

def cargar_historial_web_desde_archivo(ruta_archivo:str):
    """Función que carga los datos del historial web
    en una lista para poder ser mostrado posteriormente
    """
    historial_web = []
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r', encoding = "utf-8")as archi:
            lineas = archi.readlines()            
            for linea in lineas:  
                linea = linea.strip().split(',')
                nombre = linea[0]
                fraccion_correctas = linea[1]
                cant_rondas = linea[2]
                fecha = linea[3]
                historial = {}
                historial["usuario"] = nombre
                historial["aciertos"] = fraccion_correctas
                historial["num_rondas"] = cant_rondas
                historial["fecha"] = fecha              
                historial_web.append(historial)
    else:
        with open(ruta_archivo, "w", encoding="utf-8") as archi:
            pass
    return historial_web

def cargar_lista_pelis_desde_archivo(ruta_archivo:str):
    lista_pelis=[]
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r' ,encoding="utf-8") as archi:
            lineas=archi.readlines()
            for linea in lineas:
                linea = linea.strip().split(';')
                peli = linea[1]
                lista_pelis.append(peli)
    else:
        with open(ruta_archivo, "w", encoding="utf-8") as archi:
            pass
    return sorted(set(lista_pelis))

def obtener_datos_para_gráfica(ruta_archivo:str):
    lista_aciertos=[]
    lista_errores=[]
    lista_fechas=[]
    datos_grafica=[]
    #Recorrer el historial
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r', encoding="utf-8") as archi:
            lineas=archi.readlines()
            for linea in lineas:
                linea = linea.strip().split(',')
                lista_aciertos.append(int(linea[1]))
                lista_errores.append(int(linea[2])- int(linea[1]))
                lista_fechas.append(str(linea[3]))                       
            aciertos_por_fecha = defaultdict(int)
            errores_por_fecha = defaultdict(int)
            for i, fecha in enumerate(lista_fechas):
                aciertos_por_fecha[fecha] += lista_aciertos[i]
                errores_por_fecha[fecha] += lista_errores[i]
            fechas_agrupadas = sorted(aciertos_por_fecha.keys())
            aciertos_agrupados = [aciertos_por_fecha[fecha] for fecha in fechas_agrupadas]
            errores_agrupados = [errores_por_fecha[fecha] for fecha in fechas_agrupadas]
            datos_grafica.append(fechas_agrupadas)
            datos_grafica.append(aciertos_agrupados)
            datos_grafica.append(errores_agrupados)
    else:
        with open(ruta_archivo, "w", encoding="utf-8") as archi:
            pass
    return datos_grafica

def Cargar_lista_desde_archivo(nombre_archivo_frases:str, listadePeliculas:dict):
    """Función que extrae los nombres y frases de las peliculas desde un archivo
    y los carga a una lista.
    """
    with open(nombre_archivo_frases, "r", encoding="utf-8") as archi:

        for linea in archi:
            pelicula = linea.rstrip().split(';')
            listadePeliculas[pelicula[0]]=pelicula[1]
            
