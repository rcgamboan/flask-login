
from flask import Flask, flash, redirect, render_template, request, url_for, flash, session
from werkzeug.security import check_password_hash , generate_password_hash
from config import config
import sqlite3 as sql
import database as db1
from model import Usuario, Productor, TipoProductor


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

    editarUsuario(  request.form['id'],
                    request.form['editusername'],  
                    request.form['editnombre'],
                    request.form['editapellido'],
                    request.form['editcosecha'],
                    request.form['editrol'])
    return redirect(url_for('admin'))

@app.route('/admin/delete',methods=['POST'])
def delete():
    eliminarUsuario(request.form['user_id'])
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
                    users = obtenerUsuarios()
                    return render_template('admin.html',users=users)

                else:
                    flash("Este nombre de usuario ya existe ")
                    users = obtenerUsuarios()
                    return render_template('admin.html',users=users)   
            else:
                users = obtenerUsuarios()
                return render_template('admin.html',users=users)
        else:
            return redirect(url_for('home'))
    else:
       return redirect(url_for('login'))

# Se obtienen los datos de los productores
@app.route('/productor',methods=['GET','POST','PUT'])
def productor():

    if 'username' in session:
        if session['rol'] == 0:
            if request.method=='POST':
                
                new_prod = db1.session.query(Productor).filter_by(id = request.form['id']).first()

                if new_prod == None:
                    agregarProductor(request.form["id"], 
                                    request.form["nombres"],
                                    request.form["apellidos"],
                                    request.form["telefonoCelular"],
                                    request.form["telefonoLocal"],
                                    request.form["direccion"],
                                    request.form["direccion2"],
                                    request.form["tipo"],)
                    productores = obtenerProductores()
                    tipos = obtenerTiposProductores()
                    return render_template('productor.html',productores=productores, tipos=tipos)

                else:
                    flash("El productor ya existe ")
                    productores = obtenerProductores()
                    tipos = obtenerTiposProductores()
                    return render_template('productor.html',productores=productores, tipos=tipos)
            else:
                productores = obtenerProductores()
                tipos = obtenerTiposProductores()
                return render_template('productor.html',productores=productores, tipos=tipos)
        else:
            return redirect(url_for('home'))
    else:
       return redirect(url_for('login'))


@app.route('/productor/update',methods=['POST'])
def prod_update():

    editarProductor(
        request.form['editcedula'],
        request.form['editnombre'],
        request.form['editapellido'],
        request.form['edittelefonoC'],
        request.form['edittelefonoL'],
        request.form['editdireccion'],
        request.form['editdireccion2'],
        request.form['edittipo']
    )
    return redirect(url_for('productor'))

@app.route('/productor/delete',methods=['POST'])
def prod_eliminar():
    eliminarProductor(request.form['prodid'])
    return redirect(url_for('productor'))

@app.route('/tipoProductor', methods=['GET','POST','PUT'])
def tipo_prod():

    if 'username' in session:
        if session['rol'] == 0:
            if request.method=='POST':
                
                new_tipo = db1.session.query(TipoProductor).filter_by(direccion = request.form['direccion']).first()
                
                if new_tipo == None:
                    agregarTipoProductor(request.form['direccion'])
                    tipos = obtenerTiposProductores()
                    return render_template('tipo.html', tipos=tipos)

                else:
                    flash("El tipo de productor ya existe ")
                    tipos = obtenerTiposProductores()
                    return render_template('tipo.html', tipos=tipos)
            else:
                tipos = obtenerTiposProductores()
                return render_template('tipo.html', tipos=tipos)
        else:
            return redirect(url_for('home'))
    else:
       return redirect(url_for('login'))


@app.route('/tipoProductor/update',methods=['POST'])
def tipo_prod_update():

    #print(request.form['editid'])
    editarTipoProductor(
        request.form['editid'],
        request.form['editdescripcion'],
    )
    return redirect(url_for('tipo_prod'))

@app.route('/tipoProductor/delete',methods=['POST'])
def tipo_prod_eliminar():
    eliminarTipoProductor(request.form['tipoid'])
    return redirect(url_for('tipo_prod'))

# Metodo que retorna todos los registros de la tabla productores
def obtenerProductores():
    productores = db1.session.query(Productor).filter_by().all()
    return productores

# Metodo que retorna todos los registros de la tabla usuarios
def obtenerUsuarios():
    usuarios = db1.session.query(Usuario).filter_by().all()
    return usuarios

# Metodo que retorna todos los registros de la tabla tipoproductor
def obtenerTiposProductores():
    tiposProductores = db1.session.query(TipoProductor).filter_by().all()
    return tiposProductores

def editarUsuario(id,username = "", nombres = "",apellidos = "",cosecha = "",rol = -1):

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
        
        if rol != -1 and rol != None:
            user.rol = rol

        

        db1.session.commit()
    else:
        flash("El usuario no existe")

def editarProductor(id,nombres = "",apellidos = "",telefonoCelular = "",telefonoLocal = "",direccion = "",direccion2 = "",tipo = ""):

    productor = db1.session.query(Productor).filter_by(id = id).first()
    
    if productor != None:
        
        if nombres != "" and nombres != None:            
            productor.nombres = nombres

        if apellidos != "" and apellidos != None:
            productor.apellidos = apellidos
        
        if telefonoCelular != "" and telefonoCelular != None:
            productor.telefonoCelular = telefonoCelular
        
        if telefonoLocal != "" and telefonoLocal != None:
            productor.telefonoLocal = telefonoLocal
        
        if direccion != "" and direccion != None:
            productor.direccion = direccion
        
        if direccion2 != "" and direccion2 != None:
            productor.direccion2 = direccion2
        
        if tipo != "" and tipo != None:
            productor.tipo = tipo

        db1.session.commit()
    else:
        flash("El productor no existe")

def editarTipoProductor(id,direccion = ""):

    tipoProductor = db1.session.query(TipoProductor).filter_by(id = id).first()
    
    if tipoProductor != None:
        
        if direccion != "" and direccion != None:            
            tipoProductor.direccion = direccion

        db1.session.commit()
    else:
        flash("El tipo no existe")

# Recibe el username y la contraseña del usuario a crear
# Se llama a la sesion de SQLAlchemy y se crea el usuario
def agregarUsuario(username,password,nombres,apellidos,cosecha,rol,inicio = 1):

    logged_user = db1.session.query(Usuario).filter_by(username = username).first()

    if logged_user == None:
        user = Usuario(username, generate_password_hash(password),nombres,apellidos,cosecha,rol)
        db1.session.add(user)
        db1.session.commit()
    else:
        if inicio != 1:
            return
        else:
            flash("El usuario ya se encuentra registrado")

def agregarProductor(id, nombres,apellidos,telefonoCelular,telefonoLocal,direccion,direccion2,tipo):

    tipos = db1.session.query(TipoProductor).filter_by().all()
    if len(tipos) == 0:
        flash("Debe agregar un tipo de productor primero")
        return
    else:
        prod = Productor(id, nombres,apellidos,telefonoCelular,telefonoLocal,direccion,direccion2,tipo)
        db1.session.add(prod)
        db1.session.commit()

def agregarTipoProductor(descripcion):
    tipo = TipoProductor(descripcion)
    print(tipo)
    db1.session.add(tipo)
    db1.session.commit()

def eliminarUsuario(ID):
    
    if int(session['id']) == int(ID):
        flash("No se puede eliminar esta cuenta mientras tiene una sesion activa")
        return
    else:
        admins = db1.session.query(Usuario).filter_by(rol=1).all()
        if len(admins) == 1:
            flash("No se puede eliminar esta cuenta ya que no hay otros administradores")
            return
        else:
            db1.session.query(Usuario).filter_by(id=ID).delete()
            db1.session.commit()

def eliminarProductor(ID):
    db1.session.query(Productor).filter_by(id=ID).delete()
    db1.session.commit()

def eliminarTipoProductor(ID):
    productores =  db1.session.query(Productor).filter_by(tipo=ID).all()
    print(productores)
    if len(productores) > 0:
        flash("No se puede eliminar ya que existe por lo menos un productor asociado a este tipo")
        return
    else:
        db1.session.query(TipoProductor).filter_by(id=ID).delete()
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
    agregarUsuario("admin","admin","admin","admin","Enero - Marzo 2022",1,0)
    app.run()

