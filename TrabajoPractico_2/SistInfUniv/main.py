from modules.instituciones import Facultad, Curso, Departamento
from modules.recursos_humanos import Estudiante, Profesor
import os

docentes_iniciales = {}
alumnos_iniciales = {}
director_inicial=Profesor('Gastón Gonzalez','17952494')
facultad = Facultad('FIUNER','Informática',director_inicial)

def mostrar_menu():
    print(
        """
        ######################################
        #Sistema de información universitaria#
        ######################################
        1 - Inscribir alumno
        2 - Contratar profesor
        3 - Crear departamento nuevo
        4 - Crear curso nuevo
        5 - Inscribir estudiante a un curso
        6 - Salir
        """
    )
    
def cargar_datos_iniciales():
    nombres=[]
    documentos=[]
    ruta_archivo = './data/datosiniciales.txt'
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r', encoding="utf-8") as archi:
            lineas = archi.readlines()
            for linea in lineas:
                linea = linea.strip().split(',')
                nombres.append(linea[0])
                documentos.append(linea[1])
            for i in range(4):
                docentes_iniciales[documentos[i]] = Profesor(nombres[i],documentos[i])#Los docentes existen por fuera de la facultad
                facultad.agregarDocente(docentes_iniciales[documentos[i]])
            for i in range(4,8):
                alumnos_iniciales[documentos[i]]=Estudiante(nombres[i],documentos[i])#Los estudiantes existen por fuera de la facultad
                facultad.agregarEstudiante(alumnos_iniciales[documentos[i]])
                          
                    
# Función principal
if __name__ == '__main__':
    cargar_datos_iniciales()
    print(f"Los DNI de los docentes que trabajan en la facultad son: {', '.join(facultad.docentes)}")
    print(f"Los DNI de los estudiantes que tiene la facultad son: {', '.join(facultad.estudiantes)}")
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Elija una opción: "))
            
            if opcion == 1:
                nombre=input("Ingrese el nombre del alumno: ")
                DNI = input("Ingrese el DNI del alumno: ")
                alumno = Estudiante(nombre,DNI)
                facultad.agregarEstudiante(alumno)
                print(facultad.estudiantes)
                
            elif opcion == 2:
                nombre=input("Ingrese el nombre del docente: ")
                DNI=input("ingrese el DNI del docente: ")
                docente=Profesor(nombre,DNI)
                facultad.agregarDocente(docente)
                print(facultad.docentes)
                
            elif opcion == 3:
                nombre_depto = input("Ingrese el nombre del departamento: ")
                DNI_director = input("Ingrese el DNI del director de entre los docentes presentes: ")
                if DNI_director in facultad.docentes:
                    facultad.crearDepartamento(nombre_depto,DNI_director)
                    print(f"Los departamentos existentes son: {', '.join(facultad.deptos)}")        
                    
            elif opcion == 4:
                nombre_depto = input("Ingrese el nombre del departamento donde va a agregar el curso: ")
                curso_elegido = input("Ingrese el nombre del curso: ")
                DNI_titular = input("Ingrese el DNI del titular de entre los docentes que trabajan en la facultad: ")
                facultad.agregar_curso_a_depto(nombre_depto,curso_elegido,DNI_titular)
                print(f"Los cursos presentes en el departamento son:{', '.join(facultad.mostrar_cursos_de_un_depto(nombre_depto))}")

            elif opcion == 5:
                DNI_estudiante = input("Ingrese el DNI del estudiante a inscribir de entre los estudiantes inscriptos a la facultad: ")
                nombre_depto = input("Ingrese el nombre del departamento donde está el curso de interés: ")
                nombre_curso = input("Ingrese el nombre del curso de interés: ")
                facultad.inscribir_estudiante_a_un_curso(DNI_estudiante,nombre_depto,nombre_curso)
                print("El estudiante está inscripto a: ")
                print(f"{facultad.mostrar_cursos_de_un_estudiante(DNI_estudiante)}")
            elif opcion == 6:
                print("Saliendo del sistema.")
                break
            else:
                print("Opción inválida.")
        except ValueError:
            print("Ingrese una opción válida.")
