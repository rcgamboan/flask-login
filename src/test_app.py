import unittest
import database as db1
from flask import Flask, flash, redirect, render_template, request, url_for, flash
from werkzeug.security import check_password_hash , generate_password_hash
from model import Usuario
from app import app

class Test(unittest.TestCase):

    # Prueba iniciar sesion con usuario que no existe
    # Al buscar el usuario en la BD, retorna none porque no se encuentra agregado
    def test_login0(self):
        self.assertEqual( login("prueba0","prueba0"), "El usuario no existe")
    
    # Prueba iniciar sesion con credenciales validas
    def test_login1(self):
        agregarUsuario(12345,"rgcn","rgcn","nombre1","apellido1",416123456,21233534,"caracas",1)
        self.assertEqual( login("rgcn","rgcn"), "Se ha iniciado sesion como administrador!")
    
    # Prueba iniciar sesion como usuario normal
    def test_login2(self):
        agregarUsuario(236745,"prueba2","prueba2","nombre2","apellido2",416123456,21233534,"caracas",0)
        self.assertEqual(login("prueba2","prueba2"), "Se ha iniciado sesion como usuario normal!")

    # Prueba agregar usuario normal
    # Se agrega el usuario y se verifica que este se encuentre en la BD
    def test_agregar0(self):
        agregarUsuario(21314,"test_agregar0","test_agregar0","nombre3","apellido3",454354,57535354,"caracas",0)
        usuarioDB = db1.session.query(Usuario).filter_by(username = "test_agregar0").first()
        self.assertEqual("test_agregar0" , usuarioDB.username)
    
    # Prueba eliminar usuario existente
    def test_eliminar0(self):
        agregarUsuario(21314,"test_eliminar0","test_eliminar0","nombre4","apellido4",454354,57535354,"caracas",0)
        eliminarUsuario(2134)
        usuarioDB = db1.session.query(Usuario).filter_by(username = "test_agregar0").first()
        self.assertIsNone(usuarioDB)
    
    # Prueba eliminar usuario no existente
    def test_eliminar1(self):
        self.assertEqual(eliminarUsuario(99999),"El usuario no existe")
    
    # Prueba editar usuario existente
    # Se agrega un usuario y se modifica su username y telefono celular
    def test_editar0(self):
        agregarUsuario(21314,"test_editar0","test_editar0","nombre4","apellido4",454354,57535354,"caracas",0)
        editarUsuario(username="nuevoUsername",telefonoCelular=99999)
        usuarioDB = db1.session.query(Usuario).filter_by(username = "nuevoUsername").first()
        self.assertEqual(usuarioDB.telefonoCelular,99999)
    
    # Prueba eliminar usuario no existente
    def test_eliminar1(self):
        self.assertEqual(editarUsuario(99999,password="prueba_eliminar"),"El usuario no existe")

    
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
        return "El usuario no existe"

def eliminarUsuario(id):
    logged_user = db1.session.query(Usuario).filter_by(id = id).first()
    if logged_user != None:
        user = db1.session.query(Usuario).get(id)
        db1.session.delete(user)
        db1.session.commit()
    else:
        return "El usuario no existe"

def agregarUsuario(id,username,password,nombres,apellidos,telefonoCelular,telefonoLocal,direccion,rol):

    logged_user = db1.session.query(Usuario).filter_by(id = id).first()

    if logged_user == None:
        user = Usuario(id,username, generate_password_hash(password),nombres,apellidos,telefonoCelular,telefonoLocal,direccion,rol)
        db1.session.add(user)
        db1.session.commit()
    else:
        return "El usuario ya se encuentra registrado"

def login(user,password):

    logged_user = db1.session.query(Usuario).filter_by(username = user).first()
    if logged_user != None:

        if check_password_hash(logged_user.password,password):

            if logged_user.isAdmin == 0:
                string = "Se ha iniciado sesion como usuario normal!"
                return string
            else:
                string = "Se ha iniciado sesion como administrador!"
                return string
        else:
            string = "Alguno de los datos es incorrecto"
            return string
    else:
        string = "El usuario no existe"
        return string
    

if __name__ == '__main__':
    db1.Base.metadata.create_all(db1.engine)
    unittest.main()
