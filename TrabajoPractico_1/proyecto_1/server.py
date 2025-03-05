from flask import render_template, request, redirect, url_for
import matplotlib.pyplot as plt
from modules.config import app
from modules import servicio


#El historial debe guardar el nombre del jugador, su cantidad de aciertos y la fecha y hora a la que inició el triada.
historial_web=[]
pelicula_correcta = ""
Ronda = 0
rondas=0
EsCorrecto = None
triada = {}
listadePeliculas={}
usuario = ""
lista_aux = []
datos_grafica_aux = []
frases_usadas=[]
aciertos = 0
contaAciertos = 0
contaFallos = 0
peliculas_usadas = set()
RUTA, ARCHIVOFRASES, ARCHIVOHISTORIAL= "./data/", "frases_de_peliculas.txt", "historial_web.txt"
ARCHIVOJPG, ARCHIVOPDF = "static/images/grafica.jpg", "static/pdf/grafica.pdf"

servicio.Cargar_lista_desde_archivo(RUTA+ARCHIVOFRASES, listadePeliculas)

@app.route("/", methods=['GET', 'POST'])
def home():
    global rondas, usuario, aciertos, Ronda
    usuario = ""
    rondas = 0
    aciertos=0
    Ronda=0
    if request.method == 'POST':
        usuario = request.form["usuario"]
        rondas=int(request.form["rondas"])
        return redirect(url_for('jugar'))
    return render_template('home.html', rondas = rondas, usuario = usuario)

@app.route("/historial")
def historial():
    historial_aux = servicio.obtener_historial(RUTA+ARCHIVOHISTORIAL)
    return render_template('historial.html', historial_web = historial_aux)

@app.route("/listapelis")
def listaPelis():
    lista_aux = servicio.cargar_listaPelis(RUTA+ARCHIVOFRASES)
    return render_template('listapelis.html', lista_pelis = lista_aux)

@app.route("/graficas")
def mostrarGraficas():
    datos_grafica_aux = servicio.obtener_datos_para_gráfica(RUTA+ARCHIVOHISTORIAL)
    servicio.mostrarGraficas(datos_grafica_aux,ARCHIVOJPG)
    servicio.generarPDF(ARCHIVOJPG,ARCHIVOPDF)
    return render_template('graficas.html', lista_aciertos = datos_grafica_aux[1], lista_errores = datos_grafica_aux[2],
                           lista_fechas = datos_grafica_aux[0],pdf_path=ARCHIVOPDF)

@app.route("/jugar", methods=['GET', 'POST'])
def jugar():   
    global EsCorrecto, Ronda, triada, aciertos, lista_aux, rondas, pelicula_correcta, frases_usadas, peliculas_usadas
    if request.method == 'POST':
        pelicula_correcta=triada["pelicula"]
        opcion_elegida= int(request.form['opcion'])
        #triada["opciones"][opcion_elegida -1] es la opción correspondiente a la película correcta. El "-1" es porque se cuenta desde cero.
        if pelicula_correcta == triada["opciones"][opcion_elegida -1]:
            EsCorrecto = True
            aciertos = aciertos + 1
        else:
            EsCorrecto = False
    Ronda = Ronda + 1
    print("Las frases usadas son: ",frases_usadas)
    print("Las peliculas usadas son: ",peliculas_usadas)
    print("La cantidad de frases y pelis usadas es: ", len(frases_usadas),"y", len(peliculas_usadas)) 
    triada = servicio.hacer_triada(listadePeliculas,frases_usadas,peliculas_usadas)
    frases_usadas.append(triada["frase"])
    peliculas_usadas.add(triada["pelicula"])
    if Ronda==rondas:
        servicio.guardar_historial_web(usuario, aciertos,Ronda )    
    return render_template("jugar.html",peliculaCorrecta=triada["pelicula"],frase = triada["frase"] ,
                           opciones = triada["opciones"], EsCorrecto = EsCorrecto, Ronda = Ronda, 
                           aciertos = aciertos,rondas =rondas, pelicula_correcta = pelicula_correcta)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')