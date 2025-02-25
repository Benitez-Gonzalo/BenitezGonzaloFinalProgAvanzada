import heapq

class MonticuloMadre:
    def __init__(self):
        # Montículo de máximos (valores negativos para simular montículo de máximos con heapq)
        self.__max_heap = []
        # Montículo de mínimos
        self.__min_heap = []
        
    def insertar(self, valor):
        """
        Inserta un valor en el Montículo de Mediana y balancea los montículos.
        """
        valor=int(valor)
        # Insertar en el montículo correspondiente
        if not self.__max_heap or valor <= -self.__max_heap[0]:
            heapq.heappush(self.__max_heap, -valor)  # Insertar en montículo de máximos (como valor negativo)
        else:
            heapq.heappush(self.__min_heap, valor)  # Insertar en montículo de mínimos

        # Balancear los montículos si la diferencia de tamaño es mayor a 1
        if len(self.__max_heap) > len(self.__min_heap) + 1:
            # Mover del montículo de máximos al de mínimos
            heapq.heappush(self.__min_heap, -heapq.heappop(self.__max_heap))
        elif len(self.__min_heap) > len(self.__max_heap):
            # Mover del montículo de mínimos al de máximos
            heapq.heappush(self.__max_heap, -heapq.heappop(self.__min_heap))

    def obtener_mediana(self):
        """
        Calcula y devuelve la mediana actual.
        """
        try:
            if len(self.__max_heap) == len(self.__min_heap):
                # Promedio de las raíces de los montículos
                return (-self.__max_heap[0] + self.__min_heap[0]) / 2
            # Raíz del montículo más grande
            return -self.__max_heap[0]
        except:
            return False
        
class MonticuloDeMedianaReclamosEnProceso(MonticuloMadre):
    def __init__(self):
        super().__init__()
    
class MonticuloDeMedianaReclamosResueltos(MonticuloMadre):
    def __init__(self):
        super().__init__()
