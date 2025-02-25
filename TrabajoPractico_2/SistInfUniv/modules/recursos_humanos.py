from abc import ABC

class Persona(ABC):
    def __init__(self,pNombre,pDNI):
        self.__Nombre = pNombre
        self.__DNI = pDNI
        
    @property
    def nombre(self):
        return self.__Nombre
    
    @property    
    def DNI(self):
        return self.__DNI
           
class Estudiante(Persona):
    def __init__(self,pNombre,pDNI):
        super().__init__(pNombre,pDNI)
        self.__cursos_a_los_que_pertenece = []
        
    def agregarCurso(self,pCurso):
        self.__cursos_a_los_que_pertenece.append(pCurso)
        
    def cursosDelEstudiante(self):
        lista=[]
        for i in range(len(self.__cursos_a_los_que_pertenece)):
            lista.append(self.__cursos_a_los_que_pertenece[i])
        cursos = str(', '.join(lista))
        return cursos
     
class Profesor(Persona):
    def __init__(self,pNombre,pDNI):
        super().__init__(pNombre,pDNI)
        self.__departamentos_a_los_que_pertenece = []
        self.__cursos_a_los_que_pertenece = []
        
    def agregarDepartamento(self,pDepto:str):
        self.__departamentos_a_los_que_pertenece.append(pDepto)
        
    def cursos_a_los_que_pertenece(self,pCurso:str):
        self.__cursos_a_los_que_pertenece.append(pCurso)
        
    


    
    
                    
    
    
