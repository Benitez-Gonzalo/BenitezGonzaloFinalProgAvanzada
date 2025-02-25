"""La capa de dominio es la responsable de representar los conceptos específicos de la 
aplicación y sus reglas. Esta capa define cómo se deben manejar los datos y qué operaciones son validas
dentro del contexto específico de la aplicación.
La capa de dominio no debe depender de funciones y variables de flask como session, no debe depender 
de cual sea la interfaz de usuario ni de cómo se almacenan los datos.
"""

import random

def generar_triada(frases_pelis, frases_usadas, peliculas_usadas):
    """Genera y devuelve un diccionario con la frase y película correctas junto con las opciones adicionales."""
    opciones = []

    # Evitar frases repetidas
    frases = list(set(frases_pelis.keys()))
    pelis = list(set(frases_pelis.values()))
    
    frases_disponibles = [frase for frase in frases if frase not in frases_usadas]

    # Filtrar las películas que ya han sido usadas
    pelis_disponibles = [peli for peli in pelis if peli not in peliculas_usadas]

    # Elegir una frase y su película correspondiente
    frase_correcta = random.choice(frases_disponibles)
    peli_correcta = frases_pelis[frase_correcta]

    if peli_correcta not in pelis_disponibles:
        raise ValueError("No quedan suficientes películas no repetidas para generar una nueva ronda.")

    pelis_disponibles.remove(peli_correcta)

    for _ in range(3):  # Generar 3 opciones adicionales
        opcion = random.choice(pelis_disponibles)
        opciones.append(opcion)
        pelis_disponibles.remove(opcion)

    opciones.append(peli_correcta) 
    random.shuffle(opciones)

    triada = {"frase": frase_correcta, "pelicula": peli_correcta, "opciones": opciones}
    return triada



