from flask import render_template
from flask import render_template, request, redirect, url_for, session
from modules.config import app
from modules.servicio import *
from modules.formularios import FormLogin,FormRegistro
from datetime import datetime
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')

try:
    registrar_jefes(mails_jefes_depto,mail_sec_tecnico)
except:
    pass

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

@app.route("/", methods = ["GET","POST"])
def inicio():
    if 'username' in session and GestorLogin.usuario_autenticado:
        username = session['username']        
    else:
        username = 'Invitado'
        
    return render_template("inicio.html", user=username)

@app.route("/signup", methods=["GET","POST"])

@app.route("/signup", methods= ["GET", "POST"])
def signup():
    form_registro=FormRegistro()
    if form_registro.validate_on_submit():
        try:
            registrar(form_registro)
        except:
            flash("El usuario ya está registrado")
            return redirect(url_for('signup'))    
        else:
            flash("Usuario registrado con éxito")
            return redirect(url_for("login"))               
    return render_template('signup.html', form=form_registro)

@app.route("/login",methods = ["GET","POST"])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        
        usuario = gestor_usuarios.autenticar_usuario(form_login.email.data,form_login.contraseña.data)
        if usuario:
            gestor_login.login_usuario(usuario)
        else:
            flash("El correo y/o la contraseña son incorrectos.")
            return render_template('login.html',form=form_login)
            
        #Guardamos la info del usuario en la sesión actual:
        session['username'] = gestor_login.nombre_usuario_actual
        session['user_id'] = gestor_login.id_usuario_actual
        session['email'] = gestor_login.mail

        #Gestión de administradores:
        if session['email'] in mails_jefes_depto or session['email']==mail_sec_tecnico:
            #departamento = session['email'].split('@')[0]
            return redirect(url_for('gestion_de_jefes'))
        else:
            return redirect(url_for('usuario_final', username=session['username']))
    
    #Si hay errores de cualquier tipo, vuelve al formulario de login    
    return render_template('login.html',form=form_login)

@app.route("/jefes", methods=['GET', 'POST'])
@gestor_login.se_requiere_login
def gestion_de_jefes():
    departamento = session['email'].split('@')[0]
    if departamento =='informatica':departamento = 'soporte informático'
    if departamento == 'sec_tecnica':departamento = 'secretaría técnica' 
    if request.method == 'POST':
        if request.form.get('accion') == 'analitica':
            # Lógica para mostrar las analíticas
            mostrar_analíticas()
            return render_template('analíticas.html',pdf_path=ARCHIVOPDF,html_path=ARCHIVOHTML)
        #Hecho
        if request.form.get('accion') == 'manejar_reclamos':
            # Cargar los registros del departamento
            if departamento == 'secretaría técnica': 
                reclamos = listar_todos_los_reclamos()
            else: 
                reclamos = gestor_reclamos.devolver_reclamos_segun_departamento(departamento)
            usuarios_adheridos_por_reclamo = gestor_reclamos.brindar_usuarios_adheridos_por_reclamo()
            #Modificación departamento del reclamo:
            if departamento=='secretaría técnica' and request.method == 'GET' and request.form.get('accion') == 'cambiar_departamento':
                return redirect(url_for('modificar_departamento_reclamo'))
            # Actualización estado del reclamo
            if request.method == 'POST' and request.form.get('accion') == 'cambiar_estado':
                return redirect(url_for('modificar_estado_reclamo'))    
            return render_template('manejar_reclamos.html', reclamos=reclamos, usuarios_adheridos=usuarios_adheridos_por_reclamo,departamento=departamento)
        #Hecho
        if request.form.get('accion') == 'ayuda':
            # Redirigir a la ayuda
            return render_template('ayuda.html')
        #Hecho
        if request.form.get('accion') == 'salir':
            # Cerrar sesión
            return redirect(url_for('logout'))
    # Si no se hace un POST ni GET con `resolver_reclamo`, se carga la página principal
    return render_template('jefes.html')
    
@app.route("/modificar_estado", methods=["POST"])
@gestor_login.se_requiere_login
def modificar_estado_reclamo():
    print("Entró a la función para modificar estado")
    id_reclamo = request.form.get('id_reclamo')
    nuevo_estado = request.form.get('nuevo_estado')
    tiempo_estimado = request.form.get('tiempo_estimado')
    tiempo_ocupado = request.form.get('tiempo_ocupado')
    print(f"ID Reclamo: {id_reclamo}, Nuevo Estado: {nuevo_estado}, Tiempo Estimado: {tiempo_estimado}, Tiempo Ocupado: {tiempo_ocupado}")
    if not id_reclamo or not nuevo_estado:
        flash("Faltan datos obligatorios (ID o estado).")
        return render_template("manejar_reclamos.html")  
    if nuevo_estado not in ['inválido', 'pendiente', 'en proceso', 'resuelto']:
        flash("Estado no válido.")
        return render_template("manejar_reclamos.html")
    if nuevo_estado == 'en proceso' and not tiempo_estimado:
        flash("Debe ingresar el tiempo estimado para el estado 'en proceso'.")
        return render_template("manejar_reclamos.html")
    if nuevo_estado == 'resuelto' and not tiempo_ocupado:
        flash("Debe ingresar el tiempo ocupado para el estado 'resuelto'.")
        return render_template("manejar_reclamos.html")
    try:
        resultado = actualizar_reclamo(id_reclamo, None, nuevo_estado, tiempo_estimado, tiempo_ocupado)
        if resultado:
            flash("El reclamo se actualizó correctamente.")
        else:
            flash("No se pudo actualizar el reclamo. Verifique el ID.")
    except ValueError as e:
        flash(f"Error: {str(e)}")
    return render_template("manejar_reclamos.html")

@app.route("/modificar_departamento",methods=["GET","POST"])
@gestor_login.se_requiere_login
def modificar_departamento_reclamo():
    print("Entró a la función para modificar depto")
    id_reclamo = request.args.get('id_reclamo')
    nuevo_departamento = request.args.get('nuevo_departamento')
    print(nuevo_departamento, id_reclamo, request.args)
    if nuevo_departamento:        
        actualizar_reclamo(id_reclamo, nuevo_departamento,None,None,None)
        if actualizar_reclamo:
            flash("El departamento se ha actualizado correctamente")
        else:
            flash("Ocurrió un error, no se pudo actualizar el departamento al que pertenece el reclamo.")
    else:
        flash("Ingrese un departamento válido.")
    return render_template("manejar_reclamos.html")

@app.route("/opciones_usuario_final", methods=['GET', 'POST'])
@gestor_login.se_requiere_login
def usuario_final():
    # Opción de crear un nuevo reclamo
    if request.method == 'POST' and request.form.get('accion') == 'crear_reclamo':
        # Redirige a la función de crear reclamo
        return redirect(url_for('crear_reclamo'))
    
    # Opción para listar todos los reclamos existentes o todos los reclamos de un departamento
    if request.method == 'POST' and request.form.get('accion') == 'listar_reclamos':
        departamento = request.form.get('departamento')
        reclamos_existentes = gestor_reclamos.devolver_reclamos_segun_departamento(departamento)
        diccionario_cantidad_de_asociados = cantidad_adheridos_por_reclamo()
        
        # Adhesion a un reclamo
        if request.method == 'GET' and request.args.get('accion') == 'adhesion_reclamo':
            return redirect(url_for('adherirse_a_reclamo_desde_lista'))
        # Renderizar la lista de reclamos en caso de no adherirse
        return render_template("lista_reclamos.html", lista_reclamos=reclamos_existentes, departamento=departamento, cantidad_de_asociados=diccionario_cantidad_de_asociados)

    # Opción para listar solo los reclamos del usuario actual
    if request.method == 'GET' and request.args.get('accion') == 'reclamos_propios':
        reclamos_del_usuario = gestor_usuarios.obtener_reclamos_del_usuario(session['user_id'])
        
        # Mostrar los reclamos creados o seguidos por el usuario
        return render_template("reclamos_propios.html", 
                               reclamos_del_usuario=reclamos_del_usuario)

    # Redirige al panel principal de usuario si no hay acción específica
    return render_template("opciones_usuario_final.html", user=session['username'])

@app.route("/crear_reclamo", methods=['GET', 'POST'])
@gestor_login.se_requiere_login
def crear_reclamo():
    #Acá el usuario escribe y envía el reclamo
    if request.method == 'POST':
        reclamo = request.form.get("reclamo")
        id_usuario = session['user_id']
        
        if not reclamo:
            flash("El reclamo no debe estar vacío.")
            return render_template("crear_reclamo.html")
        elif len(reclamo) > 1000:
            flash("El reclamo no debe tener más de mil caracteres")
            return render_template("crear_reclamo.html")
    
        # Llamar al gestor para agregar o encontrar reclamos similares
        reclamos_similares_o_igual = gestor_reclamos.obtener_reclamo_similar('contenido',reclamo)
        
        # Si el usuario ha presionado el botón "Crear nuevo reclamo" a pesar de haber reclamos similares
        if 'nuevo_reclamo' in request.form:
            gestor_reclamos.creación_reclamo(reclamo,id_usuario)
            flash("Reclamo creado con éxito.")
            return redirect(url_for('usuario_final'))
        # Si hay reclamos similares encontrados y el usuario no ha solicitado crear un reclamo nuevo
        elif reclamos_similares_o_igual:

            reclamo = request.form.get('reclamo') #Esto lo hace bien
            print("El reclamo es", reclamo)
            flash("Existen reclamos similares. Puedes adherirte a uno de ellos en lugar de crear uno nuevo.")
            if 'adhesion_reclamo' in request.form:
                return redirect(url_for('adherirse_a_reclamo_desde_creación'))
            return render_template("crear_reclamo.html", reclamos_similares=reclamos_similares_o_igual)
            
        # Si no hay reclamos similares, creamos el reclamo nuevo
        else:
            gestor_reclamos.creación_reclamo(reclamo,id_usuario)
            flash("Reclamo creado con éxito.")
            return redirect(url_for('usuario_final'))

    return render_template("crear_reclamo.html")

@app.route("/adhesion_reclamo_creacion", methods = ["GET","POST"])
@gestor_login.se_requiere_login
def adherirse_a_reclamo_desde_creación():
    resultado = gestor_usuarios.registrar_reclamo_a_seguir(session['user_id'],request.form.get('id_reclamo'))
    if resultado:
        flash("Adhesión al reclamo exitosa.")
    else:
        flash("Adhesión no exitosa, ya se adhirió con anterioridad.")
    return redirect(url_for('usuario_final'))

@app.route("/adhesion_reclamo_lista", methods = ["GET","POST"])
@gestor_login.se_requiere_login
def adherirse_a_reclamo_desde_lista():
    resultado = gestor_usuarios.registrar_reclamo_a_seguir(session['user_id'],request.args.get('id_reclamo'))
    if resultado:
        flash("Adhesión al reclamo exitosa.")
    else:
        flash("Adhesión no exitosa, ya se adhirió con anterioridad.")
    return render_template("lista_reclamos.html")

@app.route("/logout")
def logout():    
    gestor_login.logout_usuario()      
    session.clear()
    return redirect(url_for('inicio'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')