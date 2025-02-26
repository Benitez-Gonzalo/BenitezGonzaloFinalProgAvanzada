class MonticuloMax:
    """Montículo de máximos implementado con un arreglo."""
    def __init__(self):
        self.heap = []

    def _subir(self, indice):
        """Sube un elemento hasta su posición correcta en el montículo de máximos."""
        padre = (indice - 1) // 2
        while indice > 0 and self.heap[padre] < self.heap[indice]:
            self.heap[padre], self.heap[indice] = self.heap[indice], self.heap[padre]
            indice = padre
            padre = (indice - 1) // 2

    def _bajar(self, indice):
        """Baja un elemento hasta su posición correcta en el montículo de máximos."""
        tamano = len(self.heap)
        mayor = indice
        izq = 2 * indice + 1
        der = 2 * indice + 2

        if izq < tamano and self.heap[izq] > self.heap[mayor]:
            mayor = izq
        if der < tamano and self.heap[der] > self.heap[mayor]:
            mayor = der

        if mayor != indice:
            self.heap[indice], self.heap[mayor] = self.heap[mayor], self.heap[indice]
            self._bajar(mayor)

    def insertar(self, valor):
        """Inserta un valor en el montículo de máximos."""
        self.heap.append(valor)
        self._subir(len(self.heap) - 1)

    def extraer_maximo(self):
        """Extrae y devuelve el valor máximo (raíz) del montículo."""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        maximo = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bajar(0)
        return maximo

    def raiz(self):
        """Devuelve el valor máximo (raíz) sin extraerlo."""
        return self.heap[0] if self.heap else None

    def tamano(self):
        """Devuelve el número de elementos en el montículo."""
        return len(self.heap)


class MonticuloMin:
    """Montículo de mínimos implementado con un arreglo."""
    def __init__(self):
        self.heap = []

    def _subir(self, indice):
        """Sube un elemento hasta su posición correcta en el montículo de mínimos."""
        padre = (indice - 1) // 2
        while indice > 0 and self.heap[padre] > self.heap[indice]:
            self.heap[padre], self.heap[indice] = self.heap[indice], self.heap[padre]
            indice = padre
            padre = (indice - 1) // 2

    def _bajar(self, indice):
        """Baja un elemento hasta su posición correcta en el montículo de mínimos."""
        tamano = len(self.heap)
        menor = indice
        izq = 2 * indice + 1
        der = 2 * indice + 2

        if izq < tamano and self.heap[izq] < self.heap[menor]:
            menor = izq
        if der < tamano and self.heap[der] < self.heap[menor]:
            menor = der

        if menor != indice:
            self.heap[indice], self.heap[menor] = self.heap[menor], self.heap[indice]
            self._bajar(menor)

    def insertar(self, valor):
        """Inserta un valor en el montículo de mínimos."""
        self.heap.append(valor)
        self._subir(len(self.heap) - 1)

    def extraer_minimo(self):
        """Extrae y devuelve el valor mínimo (raíz) del montículo."""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        minimo = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bajar(0)
        return minimo

    def raiz(self):
        """Devuelve el valor mínimo (raíz) sin extraerlo."""
        return self.heap[0] if self.heap else None

    def tamano(self):
        """Devuelve el número de elementos en el montículo."""
        return len(self.heap)


class MonticuloMediana:
    """Estructura para calcular la mediana usando dos montículos."""
    def __init__(self):
        self.max_heap = MonticuloMax()  # Almacena valores menores a la mediana
        self.min_heap = MonticuloMin()  # Almacena valores mayores a la mediana
        self.mediana = 0  # Valor inicial de la mediana

    def insertar(self, valor):
        """Inserta un valor y actualiza la mediana."""
        valor = int(valor)  # Convertimos a entero como en tu implementación original
        if not self.max_heap.tamano() and not self.min_heap.tamano():
            # Si ambos montículos están vacíos, insertamos en max_heap y seteamos la mediana
            self.max_heap.insertar(valor)
            self.mediana = valor
        else:
            # Comparar con la mediana actual y decidir dónde insertar
            if valor < self.mediana:
                self.max_heap.insertar(valor)
            else:
                self.min_heap.insertar(valor)
            
            # Balancear los montículos
            if self.max_heap.tamano() > self.min_heap.tamano() + 1:
                self.min_heap.insertar(self.max_heap.extraer_maximo())
            elif self.min_heap.tamano() > self.max_heap.tamano():
                self.max_heap.insertar(self.min_heap.extraer_minimo())

            # Actualizar la mediana
            if self.max_heap.tamano() == self.min_heap.tamano():
                self.mediana = (self.max_heap.raiz() + self.min_heap.raiz()) / 2
            else:
                self.mediana = self.max_heap.raiz()

    def obtener_mediana(self):
        """Devuelve la mediana actual."""
        if not self.max_heap.tamano() and not self.min_heap.tamano():
            return False  # No hay elementos
        return self.mediana


# Clases específicas para los reclamos
class MonticuloDeMedianaReclamosEnProceso(MonticuloMediana):
    def __init__(self):
        super().__init__()

class MonticuloDeMedianaReclamosResueltos(MonticuloMediana):
    def __init__(self):
        super().__init__()
