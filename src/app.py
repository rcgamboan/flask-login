
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
                setSession(logged_user)
                
                if check_password_hash(logged_user.password,request.form['password']):

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
    #obtener tipo y con eso crear funciones para eliminar o editar segun corresponda
    #print(request.form['tipo'])
    editarUsuario(  request.form['editusername'],  
                    request.form['editnombre'],
                    request.form['editapellido'],
                    request.form['editcosecha'],
                    request.form['editrol'])
    return redirect(url_for('admin'))

@app.route('/admin/delete',methods=['POST'])
def delete():
    eliminarUsuario(request.form['id'])
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

    if request.method=='POST':
        
        new_prod = db1.session.query(Productor).filter_by(nombres = request.form['nombres']).first()

        if new_prod == None:
            agregarProductor(request.form["id"], 
                            request.form["nombres"],
                            request.form["apellidos"],
                            request.form["telefonoCelular"],
                            request.form["telefonoLocal"],
                            request.form["direccion"],
                            request.form["tipo"],)
            productores = obtenerProductores()
            tipos = obtenerTiposProductores()
            return render_template('productor.html',productores=productores, tipos=tipos)

        else:
            flash("Este producto ya existe ")
            productores = obtenerProductores()
            tipos = obtenerTiposProductores()
            return render_template('productor.html',productores=productores, tipos=tipos)
    else:
        productores = obtenerProductores()
        tipos = obtenerTiposProductores()
        return render_template('productor.html',productores=productores, tipos=tipos)


@app.route('/productor/update',methods=['POST'])
def prov_update():
    return redirect(url_for('productor'))

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

def editarUsuario(username = "", nombres = "",apellidos = "",cosecha = "",rol = -1):

    logged_user = db1.session.query(Usuario).filter_by(username = username).first()
    
    if logged_user != None:
        user = db1.session.query(Usuario).filter_by(username = username).first()

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

def editarProductor(id,nombres = "",apellidos = "",telefonoCelular = "",telefonoLocal = "",direccion = "",tipo = ""):

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
        
        if tipo != "" and tipo != None:
            productor.tipo = tipo

        db1.session.commit()
    else:
        flash("El productor no existe")

def editarTipoProductor(id,descripcion = ""):

    tipoProductor = db1.session.query(TipoProductor).filter_by(id = id).first()
    
    if tipoProductor != None:
        
        if descripcion != "" and descripcion != None:            
            tipoProductor.descripcion = descripcion

        db1.session.commit()
    else:
        flash("El tipo no existe")

# Recibe el username y la contraseña del usuario a crear
# Se llama a la sesion de SQLAlchemy y se crea el usuario
def agregarUsuario(username,password,nombres,apellidos,cosecha,rol):

    logged_user = db1.session.query(Usuario).filter_by(username = username).first()

    if logged_user == None:
        user = Usuario(username, generate_password_hash(password),nombres,apellidos,cosecha,rol)
        db1.session.add(user)
        db1.session.commit()
    else:
        flash("El usuario ya se encuentra registrado")

def agregarProductor(id, nombres,apellidos,telefonoCelular,telefonoLocal,direccion,tipo):
    prod = Productor(id, nombres,apellidos,telefonoCelular,telefonoLocal,direccion,tipo)
    db1.session.add(prod)
    db1.session.commit()

def agregarTipoProductor(descripcion):
    prod = TipoProductor(descripcion)
    db1.session.add(prod)
    db1.session.commit()

def eliminarUsuario(ID):
    print(ID)
    db1.session.query(Usuario).filter_by(id=ID).delete()
    db1.session.commit()

def eliminarTipoProductor(ID):
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
    app.run()

