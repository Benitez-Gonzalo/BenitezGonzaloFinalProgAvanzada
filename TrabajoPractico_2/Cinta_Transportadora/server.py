from flask import Flask, app, render_template, request,redirect,url_for
from modules import Alimentos as Alimentos
from modules import CintaTransp as CT
from modules import CajonDeAlimentos as CA
from modules import Calculadora as CAL 

app = Flask(__name__)
cantAlimentos=0

@app.route("/", methods=['GET', 'POST'])
def home():
    
    global cantAlimentos    
    if request.method == 'POST':
       cantAlimentos= int(request.form.get("CantAlimentos"))
       return redirect(url_for('TransporteDeAlimentos'))

    return render_template("home.html") 

@app.route("/TransporteDeAlimentos", methods=['GET', 'POST'])
def TransporteDeAlimentos():
    global cantAlimentos
    global cont 
   
    cinta = CT.CintaTransportadora()
    cajon=CA.CajonDeAlimento() 
    calculadora= CAL.Calculadora()
    cont = 0 
    while (cont<cantAlimentos):
        alimento=cinta.transportarAlimentos()
        if alimento != None : 
            cajon.agregar_alimento(alimento)
            cont+=1
    
    awAlimentos=calculadora.aw_alimentos(cajon)
 
    advertencias=[]
    for alim, aw in awAlimentos.items():

        if calculadora.awNoEsAceptable(aw):
            advertencias.append(alim)

    return render_template("TransporteDeAlimentos.html", aw_alimentos=awAlimentos, advertencias=advertencias)

if __name__ == "__main__":
    app.run(debug=True)