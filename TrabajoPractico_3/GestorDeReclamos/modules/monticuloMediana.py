#La relación de MontículoMediana con MontículoMax y MontículoMin se da mediante duck typing (polimorfismo sin herencia)

class MonticuloMax():
    """Montículo de máximos implementado con un arreglo."""
    def __init__(self):
        self.__heap = []

    def subir(self, indice):
        """Sube un elemento hasta su posición correcta en el montículo de máximos."""
        padre = (indice - 1) // 2 #La división entera nos asegura obtener siempre el índice del padre independientemente de si el hijo es el izquierdo o el derecho.
        while indice > 0 and self.__heap[padre] < self.__heap[indice]:
            self.__heap[padre], self.__heap[indice] = self.__heap[indice], self.__heap[padre] #Los intercambiamos
            indice = padre
            padre = (indice - 1) // 2 #Recalcula el nuevo padre

    def bajar(self, indice):
        """Baja un elemento hasta su posición correcta en el montículo de máximos."""
        tamano = len(self.__heap)
        mayor = indice
        izq = 2 * indice + 1
        der = 2 * indice + 2

        #izq<tamano y der<tamano es para asegurarse de que los hijos existan (que estén dentro del rango delimitado por el tamaño del montículo)
        if izq < tamano and self.__heap[izq] > self.__heap[mayor]:
            mayor = izq
        if der < tamano and self.__heap[der] > self.__heap[mayor]:
            mayor = der

        #Si mayor no es el índice original (es decir, uno de los hijos es mayor), intercambia el elemento con el hijo mayor.
        if mayor != indice:
            self.__heap[indice], self.__heap[mayor] = self.__heap[mayor], self.__heap[indice]
            #Después de intercambiar el elemento con el hijo mayor, el elemento que ahora está en la posición del hijo puede seguir violando la 
            #propiedad del montículo máximo más abajo en el árbol. Por eso, se llama a bajar(mayor) para continuar el proceso hasta que el elemento esté en su posición correcta.
            self.bajar(mayor)

    def insertar(self, valor):
        """Inserta un valor en el montículo de máximos."""
        self.__heap.append(valor)
        self.subir(len(self.__heap) - 1)

    def extraer_raiz(self):
        """Extrae y devuelve el valor máximo (raíz) del montículo."""
        if not self.__heap:
            return None
        #Si tiene un solo elemento, lo elimina y lo devuelve con pop().
        if len(self.__heap) == 1:
            return self.__heap.pop()
        #Guarda el valor máximo (self.__heap[0]) en maximo.
        maximo = self.__heap[0]
        #Reemplaza la raíz con el último elemento del arreglo (self.__heap[0] = self.__heap.pop()).
        self.__heap[0] = self.__heap.pop()
        #Llama a bajar(0) para restaurar la propiedad del montículo máximo.
        self.bajar(0)
        return maximo

    def raiz(self):
        """Devuelve el valor máximo (raíz) sin extraerlo."""
        return self.__heap[0] if self.__heap else None

    def tamano(self):
        """Devuelve el número de elementos en el montículo."""
        return len(self.__heap)


class MonticuloMin():
    """Montículo de mínimos implementado con un arreglo."""
    def __init__(self):
        self.__heap = []

    def subir(self, indice):
        """Sube un elemento hasta su posición correcta en el montículo de mínimos."""
        padre = (indice - 1) // 2
        # A diferencia de MonticuloMax, aquí la condición es self.__heap[padre] > self.__heap[indice], 
        # porque en un montículo de mínimos el padre debe ser menor que sus hijos.
        while indice > 0 and self.__heap[padre] > self.__heap[indice]:
            self.__heap[padre], self.__heap[indice] = self.__heap[indice], self.__heap[padre]
            indice = padre
            padre = (indice - 1) // 2

    def bajar(self, indice):
        """Baja un elemento hasta su posición correcta en el montículo de mínimos."""
        tamano = len(self.__heap)
        menor = indice
        izq = 2 * indice + 1
        der = 2 * indice + 2

        # A diferencia de MonticuloMax, aquí se busca el hijo menor (self.__heap[izq] < self.__heap[menor]), 
        # porque en un montículo de mínimos el padre debe ser menor que sus hijos.
        if izq < tamano and self.__heap[izq] < self.__heap[menor]:
            menor = izq
        if der < tamano and self.__heap[der] < self.__heap[menor]:
            menor = der

        if menor != indice:
            self.__heap[indice], self.__heap[menor] = self.__heap[menor], self.__heap[indice]
            self.bajar(menor)

    def insertar(self, valor):
        """Inserta un valor en el montículo de mínimos."""
        self.__heap.append(valor)
        self.subir(len(self.__heap) - 1)

    def extraer_raiz(self):
        """Extrae y devuelve el valor mínimo (raíz) del montículo."""
        if not self.__heap:
            return None
        if len(self.__heap) == 1:
            return self.__heap.pop()
        minimo = self.__heap[0]
        self.__heap[0] = self.__heap.pop()
        self.bajar(0)
        return minimo

    def raiz(self):
        """Devuelve el valor mínimo (raíz) sin extraerlo."""
        return self.__heap[0] if self.__heap else None

    def tamano(self):
        """Devuelve el número de elementos en el montículo."""
        return len(self.__heap)

#La relación de MontículoMediana con MonticuloDeMedianaReclamosEnProceso y MonticuloDeMedianaReclamosResueltos es una herencia sin polimorfismo.

class MonticuloMediana:
    """Estructura para calcular la mediana usando dos montículos."""
    def __init__(self):
        self.__max_heap = MonticuloMax()  # Almacena valores menores a la mediana
        self.__min_heap = MonticuloMin()  # Almacena valores mayores a la mediana
        self.__mediana = 0  # Valor inicial de la mediana

    def insertar(self, valor):
        """Inserta un valor y actualiza la mediana."""
        valor = int(valor)
        if not self.__max_heap.tamano() and not self.__min_heap.tamano():
            # Si ambos montículos están vacíos, inserta en max_heap y establece la mediana como el valor.
            self.__max_heap.insertar(valor)
            self.__mediana = valor
        else:
            # Comparar con la mediana actual y decidir dónde insertar
            if valor < self.__mediana:
                #Si el valor es menor que la mediana actual, lo inserta en max_heap.
                self.__max_heap.insertar(valor)
            else:
                #Si es mayor o igual, lo inserta en min_heap.
                self.__min_heap.insertar(valor)
            
            # Balancear los montículos
            if self.__max_heap.tamano() > self.__min_heap.tamano() + 1:
                #Si max_heap tiene más elementos que min_heap, se extrae el máximo de max_heap y se inserta en min_heap.
                self.__min_heap.insertar(self.__max_heap.extraer_raiz())
            elif self.__min_heap.tamano() > self.__max_heap.tamano():
                #Si min_heap tiene más elementos que max_heap, se extrae el mínimo de min_heap y se inserta en max_heap.
                self.__max_heap.insertar(self.__min_heap.extraer_raiz())

            # Actualizar la mediana
            if self.__max_heap.tamano() == self.__min_heap.tamano():
                #Si ambos montículos tienen el mismo tamaño, la mediana es el promedio de las raíces.
                self.__mediana = (self.__max_heap.raiz() + self.__min_heap.raiz()) / 2
            else:
                # Si los montículos tienen diferente tamaño, la mediana es la raíz de max_heap. Esto es porque 
                # si el número total de elementos es impar, la mediana será el elemento central, y este se almacena en la raíz de max_heap. Esto implica que max_heap debe tener un elemento más que min_heap.
                # Si el número total de elementos es par, la mediana será el promedio de los dos elementos centrales, que serán la raíz de max_heap (el mayor de la mitad inferior)
                # y la raíz de min_heap (el menor de la mitad superior). Esto implica que ambos montículos tienen el mismo número de elementos.
                # Por lo tanto, el diseño asegura que:
                # max_heap tenga el mismo número de elementos que min_heap (si el total es par).
                # max_heap tenga un elemento más que min_heap (si el total es impar).
                self.__mediana = self.__max_heap.raiz()

    def obtener_mediana(self):
        """Devuelve la mediana actual."""
        if not self.__max_heap.tamano() and not self.__min_heap.tamano():
            return "No hay datos"
        return self.__mediana


# Clases específicas para los reclamos
class MonticuloDeMedianaReclamosEnProceso(MonticuloMediana):
    def __init__(self):
        super().__init__()

class MonticuloDeMedianaReclamosResueltos(MonticuloMediana):
    def __init__(self):
        super().__init__()
