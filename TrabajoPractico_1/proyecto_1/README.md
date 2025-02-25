### Plantilla inicial de proyecto

El proyecto_1 hace al juego web de preguntas y respuestas. Las carpetas funcionales son: data, deps, modules, static y templates. Las carpetas docs, tests y apps no son utilizadas en este proyecto (la carpeta docs contiene un ejemplo genérico de UML que no tiene que ver con el proyecto). 

La carpeta data contiene el historial web y las frases de las películas con su película correspondiente, la carpeta deps contiene el .txt con las librerías necesarias para el proyecto (además de otras que no fueron necesarias, finalmente). La carpeta modules contiene los archivos config, dominio, persistencia y servicio que contienen las funciones fundamentales para la funcionalidad del proyecto, la descripción de cada archivo está comentado al inicio de cada uno excepto el config, que inicializa la app de flask. La carpeta static contiene las imágenes de bienvenida al usuario al inicio de la aplicación, las gráficas con los aciertos y errores y las gráficas en formato .pdf. La carpeta templates contiene los .html con jinja2 y finalmente el archivo server.py es donde ejecutamos el programa.

