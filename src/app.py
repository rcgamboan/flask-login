
from flask import Flask, flash, redirect, render_template, request, url_for, flash
from werkzeug.security import check_password_hash , generate_password_hash
from config import config
import sqlite3 as sql
import database as db1
from model import Usuario, Producto


app = Flask(__name__)

# Recibe el username y la contraseña del usuario a crear
# Se llama a la sesion de SQLAlchemy y se crea el usuario
def agregarUsuario(id,username,password,nombres,apellidos,telefonoCelular,telefonoLocal,direccion,rol):

    logged_user = db1.session.query(Usuario).filter_by(id = request.form['cedula']).first()

    if logged_user == None:
        user = Usuario(id,username, generate_password_hash(password),nombres,apellidos,telefonoCelular,telefonoLocal,direccion,rol)
        db1.session.add(user)
        db1.session.commit()
    else:
        flash("El usuario ya se encuentra registrado")


def eliminarUsuario(ID):
    db1.query.filter_by(id=ID).delete()
    db1.session.commit()

def agregarProducto(nombre,idProveedor,precio,descripcion = ''):
    prod = Producto(nombre, idProveedor, precio, descripcion)
    db1.session.add(prod)
    db1.session.commit()

# Si se trata de acceder al directorio raiz de la pagina se redirecciona a login
@app.route('/')
def index():
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

    if request.method=='POST':
        logged_user = db1.session.query(Usuario).filter_by(username = request.form['username']).first()

        if logged_user != None:

            if check_password_hash(logged_user.password,request.form['password']):

                if logged_user.rol == 0:
                    return render_template('home.html',nombre=logged_user.nombres)
                elif logged_user.rol == 1:
                    return redirect(url_for('admin'))
                elif logged_user.rol == 2:
                    return redirect(url_for('proveedor'))
                else:
                    return redirect(url_for('login'))
            else:
                flash("Alguno de los datos es incorrecto")
                return render_template('auth/login.html')
        else:
            flash("El usuario no existe")
            return render_template('auth/login.html')    
    else:
        return render_template('auth/login.html')

# Pagina /home, devuelve la plantilla home.html
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/admin/update',methods=['POST'])
def update():
    #obtener tipo y con eso crear funciones para eliminar o editar segun corresponda
    #print(request.form['tipo'])
    editarUsuario(int(request.form['editcedula']),
                    request.form['editusername'], 
                    request.form['editpassword'], 
                    request.form['editnombre'],
                    request.form['editapellido'],
                    request.form['edittelefonoC'],
                    request.form['edittelefonoL'],
                    request.form['editdireccion'],
                    request.form['editrol'])
    return redirect(url_for('admin'))

@app.route('/admin/delete',methods=['POST'])
def delete():
    eliminarUsuario(request.form['id'])
    return redirect(url_for('admin'))


# Para la pagina del Admin, recibe los datos del username y password del nuevo usuario
# 
@app.route('/admin',methods=['GET','POST','PUT'])
def admin():

    if request.method=='POST':
        new_user = db1.session.query(Usuario).filter_by(username = request.form['username']).first()
        #si no existe el usuario en la base de datos
        if new_user == None:
            agregarUsuario(int(request.form['cedula']),
                            request.form['username'], 
                            request.form['password'], 
                            request.form['nombre'],
                            request.form['apellido'],
                            request.form['telefonoC'],
                            request.form['telefonoL'],
                            request.form['direccion'],
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

# Se obtienen los productos del productor indicado y se pasan como datos para mostrarlos
@app.route('/proveedor',methods=['GET','POST','PUT'])
def proveedor():

    idProveedor = request.form['idProveedor']
    if request.method=='POST':
        
        new_prod = db1.session.query(Producto).filter_by(nombre = request.form['nombre']).first()

        # Tengo que obtener el id del proveedor que solicita agregar el producto y enviarlo como parametro de la funcion
        if new_prod == None:
            agregarProducto(request.form['nombre'],idProveedor , request.form['precio'],request.form['descripcion'])
            productos = obtenerProductos(idProveedor)
            return render_template('proveedor.html',productos=productos)

        else:
            flash("Este producto ya existe ")
            productos = obtenerProductos(idProveedor)
            return render_template('proveedor.html',productos=productos)   
    else:
        idProveedor = request.form['idProveedor']
        productos = obtenerProductos(idProveedor)
        return render_template('proveedor.html',productos=productos)

@app.route('/proveedor/update',methods=['POST'])
def prov_update():
    return redirect(url_for('proveedor'))
  
def actualizarRol(id,newRol):
    user = db1.session.query(Usuario).filter_by(id = id).first()
    user.rol = newRol
    db1.session.commit()

def obtenerUsuarios():
    usuarios = db1.session.query(Usuario).filter_by().all()
    return usuarios

def editarUsuario(id,username = "", password = "",nombres = "",apellidos = "",telefonoCelular = 0,telefonoLocal = 0,direccion = "",rol = -1):

    logged_user = db1.session.query(Usuario).filter_by(id = id).first()
    
    if logged_user != None:
        user = db1.session.query(Usuario).filter_by(id = id).first()
        if username != "" and username != None:
            user.username = username
        
        if password != "" and password != None:
            user.password = generate_password_hash(password)

        if nombres != "" and nombres != None:            
            user.nombres = nombres

        if apellidos != "" and apellidos != None:
            user.apellidos = apellidos
        
        if telefonoCelular != 0 and telefonoCelular != None:
            user.telefonoCelular = telefonoCelular
        
        if telefonoLocal != 0 and telefonoLocal != None:
            user.telefonoLocal = telefonoLocal
        
        if direccion != "" and direccion != None:
            user.direccion = direccion
        
        if rol != -1 and rol != None:
            user.rol = rol

        db1.session.commit()
    else:
        flash("El usuario no existe")

# Recibe el username y la contraseña del usuario a crear
# Se llama a la sesion de SQLAlchemy y se crea el usuario
def agregarUsuario(id,username,password,nombres,apellidos,telefonoCelular,telefonoLocal,direccion,rol):

    logged_user = db1.session.query(Usuario).filter_by(id = id).first()

    if logged_user == None:
        user = Usuario(id,username, generate_password_hash(password),nombres,apellidos,telefonoCelular,telefonoLocal,direccion,rol)
        db1.session.add(user)
        db1.session.commit()
    else:
        flash("El usuario ya se encuentra registrado")

def agregarProducto(nombre,idProveedor,precio,descripcion = ''):
    prod = Producto(nombre, idProveedor, precio, descripcion)
    db1.session.add(prod)
    db1.session.commit()

# Elimina el usuario por id
def eliminarUsuario(id):
    logged_user = db1.session.query(Usuario).filter_by(id = id).first()
    if logged_user != None:
        user = db1.session.query(Usuario).get(id)
        db1.session.delete(user)
        db1.session.commit()
    else:
        flash("El usuario no existe")

# Metodo que retorna los productos correspondientes al proveedor indicado
def obtenerProductos(id):
    productos = db1.session.query(Producto).filter_by(proveedor = id).all()
    return productos

if __name__ == '__main__':
    db1.Base.metadata.create_all(db1.engine)
    app.config.from_object(config['development'])
    app.run()

