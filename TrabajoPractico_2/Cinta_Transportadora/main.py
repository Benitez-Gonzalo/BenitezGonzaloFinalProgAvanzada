# Aplicación de consola
from modules import Alimentos as Alimentos
from modules import CintaTransp as CT
from modules import CajonDeAlimentos as CA
from modules import Calculadora as CAL

def main():

    cinta = CT.CintaTransportadora()
    cantAlimentos=int(input("Ingrese el número de alimentos: "))

    cinta.transportarAlimentos()
    #listaAlimentos=cinta.getAlimentos()

    cajon = CA.CajonDeAlimento()
    calculadora= CAL.Calculadora()
    cont = 0 
    while (cont<cantAlimentos):
        alimento=cinta.transportarAlimentos()
        print(f"Alimento recibido: {alimento}") 
        if alimento != None : 
            cajon.agregar_alimento(alimento)
            cont+=1
    
    awAlimentos=calculadora.aw_alimentos(cajon)

    print(f"La actividad Aw de las frutas es: {awAlimentos['aw_frutas']}")
    print(f"La actividad aAw de los kiwis es: {awAlimentos['aw_kiwis']}")
    print(f"La actividad Aw de las manzanas es: {awAlimentos['aw_manzanas']}")

    print(f"La actividad Aw de las verduras es: {awAlimentos['aw_verduras']}")
    print(f"La actividad Aw de las papas es: {awAlimentos['aw_papas']}")
    print(f"La actividad Aw de las zanahorias es: {awAlimentos['aw_zanahorias']}")

    print(f"La actividad Aw total es: {awAlimentos['aw_total']}")

    for alim, aw in awAlimentos.items():
        if calculadora.awNoEsAceptable(aw):
            print(f"La {alim} se pasa de 0,90")

if __name__ == '__main__':
    main()