"""
La capa de servicio maneja los casos de uso (las acciones que el usuario puede realizar) de la aplicación.
Coordina la interacción entre la capa de dominio y la de persistencia. 
La aplicación implementada con cualquier interfaz de usuario (web o consola) debe comunicarse solo con 
la capa de servicio es decir, solo hacer llamadas a funciones de esta capa.
"""

from modules.dominio import generar_triada
from modules.persistencia import guardar_historial_web, obtener_datos_para_gráfica, cargar_historial_web_desde_archivo, cargar_lista_pelis_desde_archivo, Cargar_lista_desde_archivo
import fpdf, matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


def obtener_historial(ruta_aux:str):
    historial = cargar_historial_web_desde_archivo(ruta_aux) 
    return historial

def cargar_listaPelis(ruta_aux:str):
    lista = cargar_lista_pelis_desde_archivo(ruta_aux)
    return lista

def obtener_datos_grafica(ruta_aux:str):
    datos_grafica = obtener_datos_para_gráfica(ruta_aux)
    return datos_grafica

def hacer_triada(frases:dict,frases_usadas,pelis_usadas):
    return generar_triada(frases,frases_usadas,pelis_usadas)

def guardar_historial(usuario:str, aciertos:str, num_rondas:str):
    return guardar_historial_web(usuario, aciertos, num_rondas)

def cargar_lista(ruta_aux:str, lista:dict):
    return Cargar_lista_desde_archivo(ruta_aux, lista)

def mostrarGraficas(datos_grafica:list, ruta_img:str):
    fechas_agrupadas, aciertos_agrupados, errores_agrupados = datos_grafica[0], datos_grafica[1], datos_grafica[2]
    fig, axis = plt.subplots(1, 2, figsize=(10, 5))
    # Gráfico de líneas
    axis[0].plot(fechas_agrupadas, aciertos_agrupados, label='Aciertos', color='green')
    axis[0].plot(fechas_agrupadas, errores_agrupados, label='Errores', color='red')
    axis[0].set_xlabel('Fecha')
    axis[0].set_ylabel('Cantidad')
    axis[0].legend()
    axis[0].set_title('Aciertos y Errores por Fecha')
    axis[0].tick_params(axis='x', rotation=45)
    # Gráfico de torta
    axis[1].pie([sum(aciertos_agrupados), sum(errores_agrupados)], labels=['Aciertos', 'Errores'],autopct='%1.1f%%',colors=['green', 'red'])
    axis[1].axis('equal')  # Para que la gráfica sea un círculo
    plt.tight_layout()   
    plt.savefig(ruta_img)
    plt.close('all')
    return datos_grafica

def generarPDF(ruta_img:str,ruta_pdf:str):
    pdf = fpdf.FPDF(orientation='P', unit='mm', format = 'A4')
    pdf.add_page()
    pdf.image(ruta_img,type='JPG',x=10,y=10,w=190)
    pdf.output(ruta_pdf)
    



