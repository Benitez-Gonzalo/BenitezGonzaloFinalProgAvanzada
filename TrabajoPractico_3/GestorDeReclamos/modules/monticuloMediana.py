#La relación de MontículoMediana con MontículoMax y MontículoMin se da mediante duck typing (polimorfismo sin herencia)

class MonticuloMax:
    """Montículo de máximos implementado con un arreglo."""
    def __init__(self):
        self.__heap = []

    def subir(self, indice):
        """Sube un elemento hasta su posición correcta en el montículo de máximos."""
        padre = (indice - 1) // 2 #La división entera nos asegura obtener siempre el índice del padre independientemente de si el hijo es el izquierdo o el derecho.
        while indice > 0 and self.__heap[padre] < self.__heap[indice]:
            self.__heap[padre], self.__heap[indice] = self.__heap[indice], self.__heap[padre]
            indice = padre
            padre = (indice - 1) // 2

    def bajar(self, indice):
        """Baja un elemento hasta su posición correcta en el montículo de máximos."""
        tamano = len(self.__heap)
        mayor = indice
        izq = 2 * indice + 1
        der = 2 * indice + 2

        if izq < tamano and self.__heap[izq] > self.__heap[mayor]:
            mayor = izq
        if der < tamano and self.__heap[der] > self.__heap[mayor]:
            mayor = der

        if mayor != indice:
            self.__heap[indice], self.__heap[mayor] = self.__heap[mayor], self.__heap[indice]
            self.bajar(mayor)

    def insertar(self, valor):
        """Inserta un valor en el montículo de máximos."""
        self.__heap.append(valor)
        self.subir(len(self.__heap) - 1)

    def extraer_raiz(self):
        """Extrae y devuelve el valor máximo (raíz) del montículo."""
        if not self.__heap:
            return None
        if len(self.__heap) == 1:
            return self.__heap.pop()
        maximo = self.__heap[0]
        self.__heap[0] = self.__heap.pop()
        self.bajar(0)
        return maximo

    def raiz(self):
        """Devuelve el valor máximo (raíz) sin extraerlo."""
        return self.__heap[0] if self.__heap else None

    def tamano(self):
        """Devuelve el número de elementos en el montículo."""
        return len(self.__heap)


class MonticuloMin:
    """Montículo de mínimos implementado con un arreglo."""
    def __init__(self):
        self.__heap = []

    def subir(self, indice):
        """Sube un elemento hasta su posición correcta en el montículo de mínimos."""
        padre = (indice - 1) // 2
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
        valor = int(valor)  # Convertimos a entero como en tu implementación original
        if not self.__max_heap.tamano() and not self.__min_heap.tamano():
            # Si ambos montículos están vacíos, insertamos en max_heap y seteamos la mediana
            self.__max_heap.insertar(valor)
            self.__mediana = valor
        else:
            # Comparar con la mediana actual y decidir dónde insertar
            if valor < self.__mediana:
                self.__max_heap.insertar(valor)
            else:
                self.__min_heap.insertar(valor)
            
            # Balancear los montículos
            if self.__max_heap.tamano() > self.__min_heap.tamano() + 1:
                self.__min_heap.insertar(self.__max_heap.extraer_raiz())
            elif self.__min_heap.tamano() > self.__max_heap.tamano():
                self.__max_heap.insertar(self.__min_heap.extraer_raiz())

            # Actualizar la mediana
            if self.__max_heap.tamano() == self.__min_heap.tamano():
                self.__mediana = (self.__max_heap.raiz() + self.__min_heap.raiz()) / 2
            else:
                self.__mediana = self.__max_heap.raiz()

    def obtener_mediana(self):
        """Devuelve la mediana actual."""
        if not self.__max_heap.tamano() and not self.__min_heap.tamano():
            return False  # No hay elementos
        return self.__mediana


# Clases específicas para los reclamos
class MonticuloDeMedianaReclamosEnProceso(MonticuloMediana):
    def __init__(self):
        super().__init__()

class MonticuloDeMedianaReclamosResueltos(MonticuloMediana):
    def __init__(self):
        super().__init__()
