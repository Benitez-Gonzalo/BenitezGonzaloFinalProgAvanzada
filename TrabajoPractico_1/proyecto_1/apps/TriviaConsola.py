# Aplicación principal

from modules import modulo1
from modules import doc_trivia
import datetime

listadePeliculas={}
HistorialOpciones=[]

TextoMenu="""          
                        ███╗░░░███╗░█████╗░██╗░░░██╗██╗███████╗
                        ████╗░████║██╔══██╗██║░░░██║██║██╔════╝
                        ██╔████╔██║██║░░██║╚██╗░██╔╝██║█████╗░░
                        ██║╚██╔╝██║██║░░██║░╚████╔╝░██║██╔══╝░░
                        ██║░╚═╝░██║╚█████╔╝░░╚██╔╝░░██║███████╗
                        ╚═╝░░░░░╚═╝░╚════╝░░░░╚═╝░░░╚═╝╚══════╝
                       Elige una opción
                       1 - Mostrar lista de películas.
                       2 - ¡Trivia de película!
                       3 - Mostrar secuencia de opciones seleccionadas previamente.
                       4 - Borrar historial de opciones.
                       5 - Salir
                        ████████╗██████╗░██╗██╗░░░██╗██╗░█████╗░
                        ╚══██╔══╝██╔══██╗██║██║░░░██║██║██╔══██╗
                        ░░░██║░░░██████╔╝██║╚██╗░██╔╝██║███████║
                        ░░░██║░░░██╔══██╗██║░╚████╔╝░██║██╔══██║
                        ░░░██║░░░██║░░██║██║░░╚██╔╝░░██║██║░░██║
                        ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░░╚═╝░░░╚═╝╚═╝░░╚═╝
                       Tu eleccion: """
salir=False
RUTA = "./data/"
ARCHIVOFRASES = "frases_de_peliculas.txt"
ARCHIVOHIST="historial_de_opciones.txt"
try:
    modulo1.Cargar_lista_desde_archivo( RUTA + ARCHIVOFRASES, listadePeliculas)
    modulo1.Cargar_historial_desde_archivo(RUTA+ARCHIVOHIST, HistorialOpciones)             
except FileNotFoundError:
    with open(RUTA + ARCHIVOFRASES, "w") as archi:
        pass
    
while not salir:
    opcion_menu = input(TextoMenu) 
     
    if opcion_menu== "1":
        if len(listadePeliculas)== 0:
            print("La lista de peliculas está vacía")
        else:
            ListaAMostrar=modulo1.OrdenarPeliculas(listadePeliculas)
            print ("Peliculas:\n")
            
            for i in range(0,len(ListaAMostrar)):
                print(f"{i+1}_{ ListaAMostrar[i]} \n ")

        fecha_y_hora=datetime.datetime.today()
        HistorialOpciones.append(f"""Opcion 1 Fecha y hora:{
                            fecha_y_hora.strftime('%d/%m/%Y %H:%M')} """)

    elif opcion_menu == "2":
         num_rondas=int(input("Ingrese el número de rondas: "))
         doc_trivia.trivia_consola(num_rondas,listadePeliculas)  
         fecha_y_hora=datetime.datetime.today()
         HistorialOpciones.append(f"""Opcion 2 Fecha y hora:{
                            fecha_y_hora.strftime('%d/%m/%Y %H:%M')} """)

    elif opcion_menu == "3":
            modulo1.MostrarHistorial(HistorialOpciones)
            fecha_y_hora=datetime.datetime.today()
            HistorialOpciones.append(f"""Opcion 3 Fecha y hora:{
                            fecha_y_hora.strftime('%d/%m/%Y %H:%M')} """)


    elif opcion_menu == "4":
        modulo1.BorrarHistorial(HistorialOpciones)
        print("Se ha borrado el historial")
  
    elif opcion_menu== "5":
        modulo1.GuardarHistorial(RUTA+ARCHIVOHIST,HistorialOpciones)
        fecha_y_hora=datetime.datetime.today()
        HistorialOpciones.append(f"""Opcion 5 Fecha y hora:{
                            fecha_y_hora.strftime('%d/%m/%Y %H:%M')} """)
        
        print("""Gracias por jugar, nos vemos!""")
        salir=True
        exit()
    else:
        print("Opcion invalida")


