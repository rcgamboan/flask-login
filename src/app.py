import datetime
from flask import Flask, flash, redirect, render_template, request, url_for, flash, session
from sqlalchemy import null
from werkzeug.security import check_password_hash , generate_password_hash
from config import config
import sqlite3 as sql
import database as db1
from model import Compra, Usuario, Recolector, TipoRecolector, Cosecha, Evento


app = Flask(__name__)

# Si se trata de acceder al directorio raiz de la pagina se redirecciona a login
# al menos que haya una sesion iniciada, en ese caso, se redirecciona al home
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

# Para la pagina de login, recibe los datos del username y password
# cada vez que se presiona el boton en la pagina de login
# con estos datos se realiza un query en la BD
# si el query retorna None es que el usuario no existe
# caso contrario retorna un objeto tipo Usuario
# y con este objeto se compara si la contraseña suministrada es la almacenada en la BD
# si todos los datos concuerdan se redirecciona a home o a la pagina de admin segun corresponda
@app.route('/login',methods=['GET','POST'])
def login():

    if 'username' in session:
        return redirect(url_for('home'))
    else:

        if request.method=='POST':
            logged_user = db1.session.query(Usuario).filter_by(username = request.form['username']).first()
            
            if logged_user != None:
                
                if check_password_hash(logged_user.password,request.form['password']):
                    setSession(logged_user)
                    return render_template('home.html')

                else:
                    flash("Alguno de los datos es incorrecto")
                    return render_template('auth/login.html')
            else:
                flash("El usuario no existe")
                return render_template('auth/login.html')    
        else:
            return render_template('auth/login.html')

@app.route('/login/update',methods=['POST'])
def updatePasswd():

    cambiarPassword(request.form['username'],
                    request.form['oldpassword'],  
                    request.form['newpassword']
                    )
    agregarEvento(request.form['username'],"Modificacion de contraseña","Inicio de Sesion",datetime.datetime.now())
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('username', None)
    session.pop('nombres', None)
    session.pop('apellidos', None)
    session.pop('cosecha', None)
    session.pop('rol', None)
    
    return redirect('/')

# Pagina /home, devuelve la plantilla home.html
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/admin/update',methods=['POST'])
def update():
    print(request.form['id'])
    editarUsuario(  request.form['id'],
                    request.form['editusername'],  
                    request.form['editnombre'],
                    request.form['editapellido'],
                    request.form['editcosecha'],
                    request.form['editrol'])
    agregarEvento(session['username'],"Modificar","Usuario",datetime.datetime.now())
    return redirect(url_for('admin'))

@app.route('/admin/delete',methods=['POST'])
def delete():
    eliminarUsuario(request.form['user_id'])
    agregarEvento(session['username'],"Eliminar","Usuario",datetime.datetime.now())
    return redirect(url_for('admin'))

# Para la pagina del Admin, recibe los datos del username y password del nuevo usuario
@app.route('/admin',methods=['GET','POST','PUT'])
def admin():
    if 'username' in session:
        if session['rol'] == 1:
            if request.method=='POST':
                new_user = db1.session.query(Usuario).filter_by(username = request.form['username']).first()
                #si no existe el usuario en la base de datos
                if new_user == None:
                    agregarUsuario( request.form['username'], 
                                    request.form['password'], 
                                    request.form['nombre'],
                                    request.form['apellido'],
                                    request.form['cosecha'],
                                    request.form['rol'])
                    agregarEvento(session['username'],"Agregar","Usuario",datetime.datetime.now())
                    users = obtenerUsuarios()
                    return render_template('admin.html',users=users,cosechas=obtenerCosechas())

                else:
                    flash("Este nombre de usuario ya existe ")
                    users = obtenerUsuarios()
                    return render_template('admin.html',users=users,cosechas=obtenerCosechas())   
            else:
                users = obtenerUsuarios()
                return render_template('admin.html',users=users,cosechas=obtenerCosechas())
        else:
            return redirect(url_for('home'))
    else:
       return redirect(url_for('login'))

# Para la pagina del Admin, recibe los datos del username y password del nuevo usuario
@app.route('/eventos',methods=['GET','POST','PUT'])
def eventos():
    if 'username' in session:
        if session['rol'] == 1:
            eventos = obtenerEventos()
            print(eventos)
            return render_template('eventos.html',eventos=eventos)
        else:
            return redirect(url_for('home'))
    else:
       return redirect(url_for('login'))

@app.route('/eventos/delete',methods=['POST'])
def eventos_eliminar():
    eliminarEvento(request.form['event_id'])
    return redirect(url_for('eventos'))

# Se obtienen los datos de las cosechas
@app.route('/cosechas',methods=['GET','POST','PUT'])
def cosechas():
    if 'username' in session:
        if session['rol'] == 1 or session['rol'] == 0:
            if request.method=='POST':
                new_cosecha = db1.session.query(Cosecha).filter_by(descripcion = request.form['descripcion']).first()
                #si no existe la cosecha en la db
                if new_cosecha == None:
                    agregarCosecha( request.form['descripcion'], 
                                    datetime.datetime.strptime(request.form['inicio'],"%Y-%m-%d"),
                                    datetime.datetime.strptime(request.form['fin'],"%Y-%m-%d"))
                    agregarEvento(session['username'],"Agregar","Cosecha",datetime.datetime.now())
                    cosechas = obtenerCosechas()
                    return render_template('cosechas.html',cosechas=cosechas)

                else:
                    flash("Esta cosecha ya existe ")
                    cosechas = obtenerCosechas()
                    return render_template('cosechas.html',cosechas=cosechas)   
            else:
                cosechas = obtenerCosechas()
                return render_template('cosechas.html',cosechas=cosechas)
        else:
            return redirect(url_for('home'))
    else:
       return redirect(url_for('login'))

@app.route('/cosechas/update',methods=['POST'])
def cosechas_update():

    editarCosecha(
        request.form['editid'],
        request.form['editDescripcion'],
        datetime.datetime.strptime(request.form['editInicio'],"%Y-%m-%d"),
        datetime.datetime.strptime(request.form['editFin'],"%Y-%m-%d")
    )
    agregarEvento(session['username'],"Modificar","Cosecha",datetime.datetime.now())
    return redirect(url_for('cosechas'))

@app.route('/cosechas/delete',methods=['POST'])
def cosechas_eliminar():
    eliminarCosecha(request.form['cosecha_id'])
    agregarEvento(session['username'],"Eliminar","Cosecha",datetime.datetime.now())
    return redirect(url_for('cosechas'))

@app.route('/cosechas/habilitar',methods=['POST'])
def cosechas_habilitar():
    print(request.form['cosecha_id'])
    activarCosecha(request.form['cosecha_id'])
    return redirect(url_for('cosechas'))

# Se obtienen los datos de las cosechas
@app.route('/cosechas/compras/<id_cosecha>',methods=['GET','POST','PUT'])
def compras(id_cosecha):
    if 'username' in session:
        if session['rol'] == 1 or session['rol'] == 0:
            cosecha = db1.session.query(Cosecha).filter_by(id = id_cosecha).first()
            tipos = obtenerTiposRecolectores()
            recolectores = obtenerRecolectores()
            compras = obtenerCompras(cosecha.id)
            if request.method=='POST':
                if recolectores != []:
                    # Hay que verificar que la fecha este dentro de la fecha de la cosecha
                    generarCompra(
                                request.form['fecha'],
                                request.form['id'],
                                request.form['cacao'],
                                request.form['cantidad'],
                                cosecha.id,
                                request.form['observaciones'],
                                request.form['humedad'],
                                request.form['merma'])
                    agregarEvento(session['username'],"Agregar","Compra",datetime.datetime.now())
                    return render_template('compras.html',recolectores=recolectores, tipos=tipos, compras=compras, cosecha=cosecha)
                else:
                    flash("No se puede agregar la compra, no existen recolectores")
                    return render_template('compras.html',recolectores=recolectores, tipos=tipos, compras=compras, cosecha=cosecha)
            else:
                return render_template('compras.html',recolectores=recolectores, tipos=tipos, compras=compras, cosecha=cosecha)
        else:
            return redirect(url_for('home'))
    else:
       return redirect(url_for('login'))

# Se obtienen los datos de los productores
@app.route('/recolector',methods=['GET','POST','PUT'])
def recolector():

    if 'username' in session:
        if session['rol'] == 0:
            if request.method=='POST':
                
                new_prod = db1.session.query(Recolector).filter_by(id = request.form['id']).first()

                if new_prod == None:
                    tipos = obtenerTiposRecolectores()
                    if tipos != []:
                        agregarRecolector(request.form["id"], 
                                        request.form["nombres"],
                                        request.form["apellidos"],
                                        request.form["telefonoCelular"],
                                        request.form["telefonoLocal"],
                                        request.form["direccion"],
                                        request.form["direccion2"],
                                        request.form["tipo"])
                        agregarEvento(session['username'],"Agregar","Recolector",datetime.datetime.now())
                        recolectores = obtenerRecolectores()
                        tipos = obtenerTiposRecolectores()
                        return render_template('recolector.html',recolectores=recolectores, tipos=tipos)
                    else:
                        flash("No se puede agregar un recolector, agregue un tipo de recolector")
                        tipos = obtenerTiposRecolectores()
                        return redirect(url_for('tipo_prod'))

                else:
                    flash("El recolector ya existe ")
                    recolectores = obtenerRecolectores()
                    tipos = obtenerTiposRecolectores()
                    return render_template('recolector.html',recolectores=recolectores, tipos=tipos)
            else:
                recolectores = obtenerRecolectores()
                tipos = obtenerTiposRecolectores()
                return render_template('recolector.html',recolectores=recolectores, tipos=tipos)
        else:
            return redirect(url_for('home'))
    else:
       return redirect(url_for('login'))

@app.route('/recolector/update',methods=['POST'])
def prod_update():

    editarRecolector(
        request.form['editcedula'],
        request.form['editnombre'],
        request.form['editapellido'],
        request.form['edittelefonoC'],
        request.form['edittelefonoL'],
        request.form['editdireccion'],
        request.form['editdireccion2'],
        request.form['edittipo']
    )
    agregarEvento(session['username'],"Modificar","Recolector",datetime.datetime.now())
    return redirect(url_for('recolector'))

@app.route('/recolector/delete',methods=['POST'])
def prod_eliminar():
    eliminarRecolector(request.form['prodid'])
    agregarEvento(session['username'],"Eliminar","Recolector",datetime.datetime.now())
    return redirect(url_for('recolector'))

@app.route('/tipoRecolector', methods=['GET','POST','PUT'])
def tipo_prod():

    if 'username' in session:
        if session['rol'] == 0:
            if request.method=='POST':
                
                new_tipo = db1.session.query(TipoRecolector).filter_by(direccion = request.form['direccion']).first()
                
                if new_tipo == None:
                    agregarTipoRecolector(request.form['direccion'])
                    agregarEvento(session['username'],"Agregar","Tipo Recolector",datetime.datetime.now())
                    tipos = obtenerTiposRecolectores()
                    return render_template('tipo.html', tipos=tipos)

                else:
                    flash("El tipo de recolector ya existe ")
                    tipos = obtenerTiposRecolectores()
                    return render_template('tipo.html', tipos=tipos)
            else:
                tipos = obtenerTiposRecolectores()
                return render_template('tipo.html', tipos=tipos)
        else:
            return redirect(url_for('home'))
    else:
       return redirect(url_for('login'))

@app.route('/tipoRecolector/update',methods=['POST'])
def tipo_prod_update():

    editarTipoRecolector(
        request.form['editid'],
        request.form['editdescripcion'],
    )
    agregarEvento(session['username'],"Modificar","Tipo Recolector",datetime.datetime.now())
    return redirect(url_for('tipo_prod'))

@app.route('/tipoRecolector/updatePrecio',methods=['POST'])
def tipo_prod_update_precio():

    #print(request.form['editidprecio'])
    #print(request.form['editprecio'])

    cambiarPrecio(
        request.form['editidprecio'],
        request.form['editprecio'],
    )
    agregarEvento(session['username'],"Modificacion de precio","Tipo Recolector",datetime.datetime.now())
    return redirect(url_for('tipo_prod'))

@app.route('/tipoRecolector/delete',methods=['POST'])
def tipo_prod_eliminar():
    eliminarTipoRecolector(request.form['tipoid'])
    agregarEvento(session['username'],"Eliminar","Tipo Recolector",datetime.datetime.now())
    return redirect(url_for('tipo_prod'))

# Metodo que retorna todos los registros de la tabla productores
def obtenerRecolectores():
    recolectores = db1.session.query(Recolector).filter_by().all()
    return recolectores

# Metodo que retorna todos los registros de la tabla usuarios
def obtenerUsuarios():
    usuarios = db1.session.query(Usuario).filter_by().all()
    return usuarios

# Metodo que retorna todos los registros de la tabla tipoRecolector
def obtenerTiposRecolectores():
    tiposRecolectores = db1.session.query(TipoRecolector).filter_by().all()
    return tiposRecolectores

def obtenerCosechas():
    cosechas = db1.session.query(Cosecha).filter_by().all()
    return cosechas

def obtenerCompras(id):
    compras = db1.session.query(Compra).filter_by(cosecha=id).all()
    return compras

def obtenerEventos():
    eventos = db1.session.query(Evento).filter_by().all()
    return eventos

def editarUsuario(id,username = "", nombres = "",apellidos = "",cosecha = "",rol = -1):
    print(f"id a editar : {id}")
    logged_user = db1.session.query(Usuario).filter_by(id = id).first()
    
    if logged_user != None:
        user = db1.session.query(Usuario).filter_by(id = id).first()

        if user.username == session['username']:
            session['username'] = username
            session['nombres'] = nombres
            session['apellidos'] = apellidos
            session['cosecha'] = cosecha
            session['rol'] = int(rol)

        if username != "" and username != None:
            user.username = username

        if nombres != "" and nombres != None:            
            user.nombres = nombres

        if apellidos != "" and apellidos != None:
            user.apellidos = apellidos
        
        if cosecha != "" and cosecha != None:
            user.cosecha = cosecha
            user.nombreCosecha = db1.session.query(Cosecha).filter_by(id=cosecha).first().descripcion
        if rol != -1 and rol != None:
            user.rol = rol

        db1.session.commit()
    else:
        flash("El usuario no existe")

def editarRecolector(id,nombres = "",apellidos = "",telefonoCelular = "",telefonoLocal = "",direccion = "",direccion2 = "",tipo = ""):

    recolector = db1.session.query(Recolector).filter_by(id = id).first()
    
    if recolector != None:
        
        if nombres != "" and nombres != None:            
            recolector.nombres = nombres

        if apellidos != "" and apellidos != None:
            recolector.apellidos = apellidos
        
        if telefonoCelular != "" and telefonoCelular != None:
            recolector.telefonoCelular = telefonoCelular
        
        if telefonoLocal != "" and telefonoLocal != None:
            recolector.telefonoLocal = telefonoLocal
        
        if direccion != "" and direccion != None:
            recolector.direccion = direccion
        
        if direccion2 != "" and direccion2 != None:
            recolector.direccion2 = direccion2
        
        if tipo != "" and tipo != None:
            recolector.tipo = tipo

        db1.session.commit()
    else:
        flash("El recolector no existe")

def editarTipoRecolector(id,direccion = "",precio = 0):

    tipoRecolector = db1.session.query(TipoRecolector).filter_by(id = id).first()
    
    if tipoRecolector != None:
        
        if direccion != "" and direccion != None:            
            tipoRecolector.direccion = direccion
        
        if precio != 0 and precio != None:            
            tipoRecolector.precio = precio

        db1.session.commit()
    else:
        flash("El tipo no existe")

def editarCosecha(id,descripcion = "", inicio = "", fin = "", activa=-1):

    cosecha = db1.session.query(Cosecha).filter_by(id = id).first()
    
    if cosecha != None:
        
        if descripcion != "" and descripcion != None:            
            cosecha.descripcion = descripcion
        
        if inicio != "" and inicio != None:            
            cosecha.inicio = inicio
        
        if fin != "" and fin != None:            
            cosecha.fin = fin
        
        if activa != -1 and activa != None:            
            cosecha.activa = activa


        db1.session.commit()
    else:
        flash("El tipo no existe")

# Recibe el username y la contraseña del usuario a crear
# Se llama a la sesion de SQLAlchemy y se crea el usuario
def agregarUsuario(username,password,nombres,apellidos,cosecha,rol,inicio = 1):

    logged_user = db1.session.query(Usuario).filter_by(username = username).first()
    cosecha = db1.session.query(Cosecha).filter_by(id=cosecha).first() 
    if cosecha == None:
        return None
    
    # no se puede agregar un usuario a cosechas inactivas
    if cosecha.activa == 0:
        flash("La cosecha seleccionada se encuentra inactiva")
        return None
    
    if logged_user == None:
        user = Usuario(username, generate_password_hash(password),nombres,apellidos,int(cosecha.id),int(rol))
        user.nombreCosecha = cosecha.descripcion
        db1.session.add(user)
        db1.session.commit()
    else:
        if inicio != 1:
            return
        else:
            flash("El usuario ya se encuentra registrado")

def agregarRecolector(id, nombres,apellidos,telefonoCelular,telefonoLocal,direccion,direccion2,tipo):
    rec = db1.session.query(Recolector).filter_by(id=id).first()
    if rec != None:
        return None
    tipos = db1.session.query(TipoRecolector).filter_by().all()
    if len(tipos) == 0:
        flash("Debe agregar un tipo de productor primero")
        return
    else:
        prod = Recolector(id, nombres,apellidos,telefonoCelular,telefonoLocal,direccion,direccion2,tipo)
        db1.session.add(prod)
        db1.session.commit()

def agregarTipoRecolector(descripcion,precio=0):

    new_tipo = db1.session.query(TipoRecolector).filter_by(direccion = descripcion).first()

    if new_tipo == None:
        tipo = TipoRecolector(descripcion,precio)
        db1.session.add(tipo)
        db1.session.commit()
    else:
        return

def agregarCosecha(descripcion, inicio = datetime.datetime.now().date(), fin = datetime.datetime.now().date(),activa = 1):

    new_cosecha = db1.session.query(Cosecha).filter_by(descripcion = descripcion).first()
    if new_cosecha != None:
        return None
    # la fecha de inicio no puede ser mayor a la del fin
    if inicio > fin:
        return None
    cosecha = Cosecha(descripcion,inicio,fin,activa)
    
    db1.session.add(cosecha)
    db1.session.commit()

def activarCosecha(id):
    cosecha = db1.session.query(Cosecha).filter_by(id=id).first()

    if cosecha.activa == 1:

        cosecha.activa = 0
        agregarEvento(session['username'],"Inhabilitar","Cosecha",datetime.datetime.now())
    else:
        cosecha.activa = 1
        agregarEvento(session['username'],"Habilitar","Cosecha",datetime.datetime.now())
    db1.session.commit()

def eliminarUsuario(ID):
    
    if int(session['id']) == int(ID):
        flash("No se puede eliminar esta cuenta mientras tiene una sesion activa")
        return
    else:
        db1.session.query(Usuario).filter_by(id=ID).delete()
        db1.session.commit()

def eliminarRecolector(ID):
    db1.session.query(Recolector).filter_by(id=ID).delete()
    db1.session.commit()

def eliminarTipoRecolector(ID):
    recolectores =  db1.session.query(Recolector).filter_by(tipo=ID).all()

    if len(recolectores) > 0:
        flash("No se puede eliminar ya que existe por lo menos un productor asociado a este tipo")
        return
    else:
        db1.session.query(TipoRecolector).filter_by(id=ID).delete()
        db1.session.commit()

def eliminarCosecha(ID):
    cosechas =  db1.session.query(Usuario).filter_by(cosecha=ID).all()

    print(cosechas)
    if len(cosechas) > 0:
        flash("No se puede eliminar ya que existe por lo menos un recolector asociado a esta cosecha")
        return
    else:
        db1.session.query(Cosecha).filter_by(id=ID).delete()
        db1.session.commit()

def eliminarEvento(ID):
    
    
    db1.session.query(Evento).filter_by(id=ID).delete()
    db1.session.commit()
    #agregarEvento(session['username'],"Eliminar","Evento",datetime.datetime.now())

def cambiarPassword(username,oldPassword,newPassword):

    usuario = db1.session.query(Usuario).filter_by(username=username).first()

    if usuario == None:
        flash("El usuario no existe")
        return
    else:

        if check_password_hash(usuario.password,oldPassword):

            usuario.password = generate_password_hash(newPassword)
            db1.session.commit()
        else:
            flash("Contraseña incorrecta")
            return

def cambiarPrecio(id,precioNuevo):
    tipoRec = db1.session.query(TipoRecolector).filter_by(id=id).first()

    if tipoRec == None:
        flash("El usuario no existe")
        return
    else:

        tipoRec.precio = precioNuevo
        db1.session.commit()

def generarCompra(fecha, cedula,cacao,cantidad,cosecha,observaciones,humedad,merma):
    recolector = db1.session.query(Recolector).filter_by(id=cedula).first()
    if recolector == None:
        flash("No existe un recolector asociado a la cedula suministrada")
        return None
    tipo_rec = db1.session.query(TipoRecolector).filter_by(id=recolector.tipo).first() 
    cosecha = db1.session.query(Cosecha).filter_by(id=cosecha).first() 

    if tipo_rec == None or cosecha == None:
        return None
    
    # no se puede generar una compra en una cosecha inactiva
    if cosecha.activa == 0:
        flash("No se pueden generar compras sobre una cosecha inactiva")
        return None

    inicio = cosecha.inicio
    fin = cosecha.fin
    fecha = datetime.datetime.strptime(fecha,"%Y-%m-%d")
    # # Si la fecha no se encuentra entre el inicio y el fin de la cosecha
    if not inicio<=fecha.date()<=fin:
        flash("la fecha de la compra no se encuentra en el periodo de la cosecha")
        return None

    compra = Compra(fecha, 
                    cedula,
                    int(recolector.tipo),
                    float(tipo_rec.precio),
                    cacao,
                    float(cantidad),
                    int(cosecha.id),
                    observaciones,
                    int(humedad),
                    int(merma))
    db1.session.add(compra)
    db1.session.commit()

def agregarEvento(usuario,descripcion,modulo,fecha):
    event = Evento(usuario, descripcion,modulo, fecha)
    print(event)
    db1.session.add(event)
    db1.session.commit()
    
#Carga los datos de usuario loggeado a la sesion actual en cache
def setSession(logged_user):
    session['id'] = logged_user.id
    session['username'] = logged_user.username
    session['nombres'] = logged_user.nombres
    session['apellidos'] = logged_user.apellidos
    session['cosecha'] = logged_user.cosecha
    session['rol'] = logged_user.rol
    

if __name__ == '__main__':
    db1.Base.metadata.create_all(db1.engine)
    app.config.from_object(config['development'])
    agregarCosecha("Ene - Mar 22")
    agregarCosecha("Sep - Dic 21")
    agregarUsuario("admin","admin","admin","admin",1,1,0)
    agregarUsuario("analista","1234","analista","analista",1,0,0)
    agregarTipoRecolector("Revendedor 2",1.5)
    agregarRecolector(26063468,"Carlos","Garcia","04124536562","04245637467","El Hatillo","El Cafetal",1)
    generarCompra("2022-07-22",26063468,"Fermentado",20,1,"Demasiado oscuro",12,3)
    app.run()
    

