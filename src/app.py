
from flask import Flask, flash, redirect, render_template, request, url_for, flash
from werkzeug.security import check_password_hash , generate_password_hash
from config import config
import sqlite3 as sql
import database as db1
from model import Usuario


app = Flask(__name__)

# Recibe el username y la contraseña del usuario a crear
# Se llama a la sesion de SQLAlchemy y se crea el usuario
def agregarUsuario(username,password,isAdmin):
    user = Usuario(username, generate_password_hash(password),isAdmin)
    db1.session.add(user)
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

                if logged_user.isAdmin == 0:
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('admin'))
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
    actualizarRol(request.form['ID'], request.form['rol'])
    return redirect(url_for('admin'))

# Para la pagina del Admin, recibe los datos del username y password del nuevo usuario
# 
@app.route('/admin',methods=['GET','POST','PUT'])
def admin():

    if request.method=='POST':
        new_user = db1.session.query(Usuario).filter_by(username = request.form['username']).first()

        #si no existe el usuario en la base de datos
        if new_user == None:
            agregarUsuario(request.form['username'], request.form['password'], request.form['isAdmin'])
            users = obtenerUsuarios()
            return render_template('admin.html',users=users)

        else:
            flash("Este nombre de usuario ya existe ")
            users = obtenerUsuarios()
            return render_template('admin.html',users=users)   
    else:
        users = obtenerUsuarios()
        return render_template('admin.html',users=users)
    
def actualizarRol(id,newRol):
    user = db1.session.query(Usuario).filter_by(id = id).first()
    user.isAdmin = newRol
    db1.session.commit()

def obtenerUsuarios():
    usuarios = db1.session.query(Usuario).filter_by().all()
    return usuarios

if __name__ == '__main__':
    db1.Base.metadata.create_all(db1.engine)
    app.config.from_object(config['development'])
    app.run()

