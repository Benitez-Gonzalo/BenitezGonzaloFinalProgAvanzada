"""
La capa de servicio maneja los casos de uso (las acciones que el usuario puede realizar) de la aplicación.
Coordina la interacción entre la capa de dominio y la de persistencia. 
La aplicación implementada con cualquier interfaz de usuario (web o consola) debe comunicarse solo con 
la capa de servicio es decir, solo hacer llamadas a funciones de esta capa.

"""

from modules.gestorReclamos import GestorDeReclamos
from modules.gestorReportes import GestorReportes
from modules.gestorUsuarios import GestorUsuarios
from modules.gestorLogin import GestorLogin
from modules.factoria import crear_repositorio, crear_reportes
from modules.config import login_manager
from modules.monticuloMediana import MonticuloDeMedianaReclamosEnProceso,MonticuloDeMedianaReclamosResueltos
from modules.graficador import Graficador
from modules.gestorEstadistico import GestorEstadistico
from flask import flash


repo_reclamos,repo_usuarios = crear_repositorio()
repoPDF,repoHTML = crear_reportes()
gestor_usuarios = GestorUsuarios(repo_usuarios)
gestor_login = GestorLogin(gestor_usuarios,login_manager)
gestor_reclamos = GestorDeReclamos(repo_reclamos)
pGestorEstadístico = GestorEstadistico(repo_reclamos)
gestorReportes = GestorReportes(repoPDF,repoHTML)
graficador = Graficador(pGestorEstadístico)


mails_jefes_depto = ['maestranza@facultad.edu.ar','informatica@facultad.edu.ar']
mail_sec_tecnico = 'sec_tecnica@facultad.edu.ar'


ARCHIVOJPG,ARCHIVOPDF,ARCHIVOHTML = "static/images/reporte.jpg","static/pdf/reporte.pdf", "static/html/reporte.html"


def registrar_jefes(mails_jefes:list,mail_secretario:str):
    usuarios_predeterminados = [
        {"nombre": "Marcos López", "nombreDeUsuario": "ML", "email": mails_jefes[0], "claustro": "PAyS", "contraseña": "1234"},
        {"nombre": "Santiago Gareis", "nombreDeUsuario": "SG", "email": mails_jefes[1], "claustro": "Docente", "contraseña": "1234"},
        {"nombre": "Pedro Díaz", "nombreDeUsuario": "PD", "email": mail_secretario, "claustro": "PAyS", "contraseña": "1234"},
    ]

    for usuario in usuarios_predeterminados:
            gestor_usuarios.registrar_nuevo_usuario(
                usuario["nombre"],
                usuario["nombreDeUsuario"],
                usuario["email"],
                usuario["claustro"],
                usuario["contraseña"],
            )

def registrar(form_registro):
    gestor_usuarios.registrar_nuevo_usuario(form_registro.nombre.data, 
                                            form_registro.nombreDeUsuario.data,
                                            form_registro.email.data,
                                            form_registro.claustro.data,
                                            form_registro.contraseña.data)
    

def obtener_usuarios_adheridos_por_reclamo():
    return repo_reclamos.obtener_usuarios_adheridos_por_reclamo()

def listar_todos_los_reclamos():
    return repo_reclamos.obtener_todos_los_registros()
    
    
def mostrar_analíticas(departamento=None):
    monticuloReclamosEnProceso,monticuloReclamosResueltos = MonticuloDeMedianaReclamosEnProceso(),MonticuloDeMedianaReclamosResueltos()
    try:
        if departamento:
            lista_tiempos_estimados, lista_tiempos_ocupados = gestor_reclamos.obtener_tiempos_por_departamento(departamento)
        else:
            lista_tiempos_estimados, lista_tiempos_ocupados = gestor_reclamos.obtener_tiempos() #Por si acaso
        for tiempo_estimado, tiempo_ocupado in zip(lista_tiempos_estimados, lista_tiempos_ocupados):
            monticuloReclamosEnProceso.insertar(tiempo_estimado)
            monticuloReclamosResueltos.insertar(tiempo_ocupado)
        graficador.mostrarGraficas(ARCHIVOJPG, monticuloReclamosEnProceso.obtener_mediana(), monticuloReclamosResueltos.obtener_mediana(), departamento)
        gestorReportes.generarReportes(ARCHIVOPDF,ARCHIVOHTML,ARCHIVOJPG)
    except:
        flash("No hay datos para generar las analíticas. Se muestra la última gráfica generada.")


def actualizar_reclamo(id_reclamo, nuevo_departamento, nuevo_estado, tiempo_estimado, tiempo_ocupado):
    kwargs = {}
    
    if nuevo_departamento:
        kwargs['departamento'] = nuevo_departamento
    if nuevo_estado:
        kwargs['estado'] = nuevo_estado
    
    if tiempo_estimado and tiempo_estimado.strip():
        try:
            tiempo_estimado = int(tiempo_estimado.strip())
            if 1 <= tiempo_estimado <= 15:
                kwargs['tiempo_estimado'] = tiempo_estimado
            else:
                flash('El tiempo estimado debe estar entre 1 y 15 días')
                return False
        except ValueError:
            flash('El tiempo estimado debe ser un número válido')
            return False
    
    if tiempo_ocupado and tiempo_ocupado.strip():
        try:
            tiempo_ocupado = int(tiempo_ocupado.strip())
            if 1 <= tiempo_ocupado <= 15:
                kwargs['tiempo_ocupado'] = tiempo_ocupado
            else:
                flash('El tiempo ocupado debe estar entre 1 y 15 días')
                return False
        except ValueError:
            flash('El tiempo ocupado debe ser un número válido')
            return False

    return gestor_reclamos.modificar_reclamo(id_reclamo, **kwargs)
            
def cantidad_adheridos_por_reclamo():
    diccionario_usuarios_adheridos = gestor_reclamos.brindar_usuarios_adheridos_por_reclamo()
    """
    Recibe un diccionario con IDs de reclamos como claves y listas de IDs de usuarios adheridos como valores.
    Retorna un nuevo diccionario con los IDs de reclamos como claves y la cantidad de adheridos como valores.
    """
    return {reclamo_id: len(usuarios) for reclamo_id, usuarios in diccionario_usuarios_adheridos.items()}


    
    
            
    



