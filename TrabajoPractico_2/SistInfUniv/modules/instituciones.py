from modules import recursos_humanos as RRHH

class Facultad():
    def __init__(self,pNombre:str,pNombreDeptoInicial:str,pDirectorInicial:RRHH.Profesor):
        self.__Nombre = pNombre
        self.__diccDeptos = {} 
        self.__diccDocentes = {}
        self.__diccDocentes[pDirectorInicial.DNI] = pDirectorInicial
        self.__diccDeptos[pNombreDeptoInicial] = Departamento(pNombreDeptoInicial,self.__diccDocentes,pDirectorInicial.DNI)
        self.__diccEstudiantes = {}
        
    def crearDepartamento(self,pNombre,pDNIDirector):
        self.__diccDeptos[pNombre] = Departamento(pNombre,self.__diccDocentes,pDNIDirector)
        self.__diccDocentes[pDNIDirector].agregarDepartamento(pNombre)
    
    @property
    def deptos(self):
        return self.__diccDeptos.keys()
    
    @property
    def docentes(self):
        return self.__diccDocentes.keys()
    
    def agregar_curso_a_depto(self,pDepto,pCurso,pDNITitular):
        if pCurso not in self.__diccDeptos[pDepto].cursos:
            self.__diccDeptos[pDepto].pedirProfesoresAfacultad(self.__diccDocentes)
            self.__diccDeptos[pDepto].agregarCurso(pCurso,pDNITitular,self.__diccDocentes)
        else:
            exit("El curso ya existe")
    
    def agregarEstudiante(self,pEstudiante:RRHH.Estudiante):
        self.__diccEstudiantes[pEstudiante.DNI] = pEstudiante
        
    @property
    def estudiantes(self):
        return self.__diccEstudiantes.keys()
    
    @property
    def nombreDocente(self):
        return self.__diccDocentes.keys()
        
    def agregarDocente(self,pDocente:RRHH.Profesor):
        self.__diccDocentes[pDocente.DNI] = pDocente
    
    @property
    def nombre(self):
        return self.__Nombre
    
    def inscribir_estudiante_a_un_curso(self,pDNIEstudiante,pDepto,pCurso):
        if pDNIEstudiante in self.__diccEstudiantes.keys():
            if pCurso in self.__diccDeptos[pDepto].cursos:
                self.__diccDeptos[pDepto].pedirEstudiantesAfacultad(self.__diccEstudiantes)
                self.__diccDeptos[pDepto].inscribirEstudianteAcurso(pDNIEstudiante,pCurso)
                self.__diccEstudiantes[pDNIEstudiante].agregarCurso(pCurso)
                
    def mostrar_cursos_de_un_depto(self,pDepto):
        lista = self.__diccDeptos[pDepto].cursos
        return lista
    
    def mostrar_cursos_de_un_estudiante(self,pDNIestudiante):
        lista = self.__diccEstudiantes[pDNIestudiante].cursosDelEstudiante()
        return lista
   
class Departamento():
    def __init__ (self,pNombreDepto:str,pDocentes:dict,pDNIDirector:str):
        self.__nombre = pNombreDepto
        self.__cursos = {}
        self.__diccAlumnos = {}
        self.__diccProfesores = pDocentes
        self.__director = self.__diccProfesores[pDNIDirector]
        
    def inscribirEstudianteAcurso(self,pDNIAlumno,pCurso):
        self.__cursos[pCurso].agregarAlumno(self.__diccAlumnos[pDNIAlumno])
    
    def agregarCurso(self,pNombreCurso:str,pDNItitular:str,pDocentes:dict):
        self.__cursos[pNombreCurso] = Curso(pNombreCurso,pDNItitular,pDocentes)
    
    def pedirProfesoresAfacultad(self,pDict:dict):
        self.__diccProfesores = pDict
    
    def pedirEstudiantesAfacultad(self,pDict:dict):
        self.__diccAlumnos = pDict
    
    @property    
    def cursos(self):
        return self.__cursos.keys()
    
    @property
    def nombre(self):
        return self.__nombre
    
    def agregarEstudiante(self,pEstudiante:RRHH.Estudiante):
        self.__diccAlumnos[pEstudiante.DNI] = pEstudiante
        
    def agregarDocente(self,pProfesor:RRHH.Profesor):
        self.__diccProfesores[pProfesor.DNI] = pProfesor 
    
    @property
    def director(self):
        return self.__director.nombre    
    
class Curso():
    def __init__(self, pNombre, pDNITitular:str,pDocentes:dict):
        self.__nombre = pNombre
        self.__docentes= pDocentes
        self.__alumnos={}
        self.__titular = self.__docentes[pDNITitular]
    
    @property    
    def nombre(self):
        return self.__nombre
    
    @property
    def titular(self):
        return self.__titular.nombre
               
    def agregarAlumno(self,pEstudiante:RRHH.Estudiante):
        self.__alumnos[pEstudiante.DNI] = pEstudiante

    def agregarDocente(self,pDocente:RRHH.Profesor,pDNI):
        self.__docentes[pDNI] = pDocente
            
    @property        
    def docentes(self):
        lista = []
        for i in range(len(self.__docentes.keys())):
            lista.append(self.__docentes.keys()[i])
        return lista
    
    @property
    def alumnos(self):
        lista = []
        for i in range(len(self.__alumnos.keys())):
            lista.append(self.__alumnos.keys()[i])
        return lista
    
    