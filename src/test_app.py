import unittest
import database as db1
from flask import Flask, flash, redirect, render_template, request, url_for, flash
from werkzeug.security import check_password_hash , generate_password_hash
from model import Usuario
from app import agregarUsuario, obtenerUsuarios, app

class Test(unittest.TestCase):

    # Prueba iniciar sesion con usuario que no existe
    # Al buscar el usuario en la BD, retorna none porque no se encuentra agregado
    def test_login0(self):
        self.assertEqual( login("prueba0","prueba0"), "El usuario no existe")
    
    # Prueba iniciar sesion como admin
    def test_login1(self):
        agregarUsuario("rgcn","rgcn",1)
        self.assertEqual( login("rgcn","rgcn"), "Se ha iniciado sesion como administrador!")
    
    # Prueba iniciar sesion como usuario normal
    def test_login2(self):
        agregarUsuario("prueba2","prueba2",0)
        self.assertEqual(login("prueba2","prueba2"), "Se ha iniciado sesion como usuario normal!")

    # Prueba agregar usuario normal
    # Se agrega el usuario y se verifica que este se encuentre en la BD
    def test_agregar0(self):
        agregarUsuario("test_agregar0","test_agregar0",0)
        usuarioDB = db1.session.query(Usuario).filter_by(username = "test_agregar0").first()
        self.assertEqual("test_agregar0" , usuarioDB.username)
    
    # Prueba agregar administrador
    # Se agrega el usuario y se verifica que este se encuentre en la BD
    def test_agregar0(self):
        agregarUsuario("test_agregar1","test_agregar1",1)
        usuarioDB = db1.session.query(Usuario).filter_by(username = "test_agregar1").first()
        self.assertEqual("test_agregar1" , usuarioDB.username)
    

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
