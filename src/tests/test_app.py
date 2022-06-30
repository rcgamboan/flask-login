from pydoc import describe
import unittest
import test_database as test_db
from test_usuario import agregarUsuario, editarUsuario, login, eliminarUsuario
from test_productor import editarProductor, agregarProductor, eliminarProductor
from test_tipo_productor import editarTipoProductor, agregarTipoProductor, eliminarTipoProductor
from test_model import Usuario, Productor, TipoProductor

class TestUsuario(unittest.TestCase):

    # Prueba iniciar sesion sin suministrar el nombre de usuario
    def test_login_sin_usuario(self):
        self.assertIsNone( login(password="prueba0"))

    # Prueba iniciar sesion sin suministrar password
    def test_login_sin_contraseña(self):
        self.assertIsNone( login(user="prueba0"))

    # Prueba iniciar sesion con usuario que no existe
    def test_login0(self):
        self.assertIsNone( login("prueba0","prueba0"))
    
    def test_login1(self):
        agregarUsuario("rgcn","rgcn","nombre","apellido","cosecha1",1)
        self.assertIsNotNone( login("rgcn","rgcn"))
    
    def test_login2(self):
        agregarUsuario("prueba2","prueba2","nombre2","apellido2","cosecha1",0)
        self.assertIsNotNone(login("prueba2","prueba2"))

    def test_agregar_sin_username(self):
        self.assertIsNone(agregarUsuario(password="test_ag",nombres="nombre3",apellidos="apellido3",cosecha="cosecha1",rol = 0))

    def test_agregar_sin_password(self):
        self.assertIsNone(agregarUsuario(username="test_ag",nombres="nombre3",apellidos="apellido3",cosecha="cosecha1",rol = 0))

    def test_agregar_sin_nombre(self):
        self.assertIsNone(agregarUsuario(username="test_ag",password="test_ag",apellidos="apellido3",cosecha="cosecha1",rol = 0))
    
    def test_agregar_sin_apellidos(self):
        self.assertIsNone(agregarUsuario(username="test_ag",password="test_ag",nombres="apellido3",cosecha="cosecha1",rol = 0))

    def test_agregar_sin_cosecha(self):
        self.assertIsNone(agregarUsuario(username="test_ag",password="test_ag",nombres="nombre",apellidos="apellido",rol = 0))

    def test_agregar_sin_rol(self):
        self.assertIsNone(agregarUsuario(username="test_ag",password="test_ag",nombres="nombre",apellidos="apellido",cosecha="cosecha1"))

    def test_agregar0(self):
        agregarUsuario("test0","test0","nombre4","apellido4","cosecha1",0)
        usuarioDB = test_db.session.query(Usuario).filter_by(username = "test0").first()
        self.assertEqual("test0" , usuarioDB.username)
    
    # Prueba eliminar usuario sin suministrar id
    def test_eliminar_sin_id(self):
        self.assertIsNone(eliminarUsuario())
    
    
    # Prueba eliminar usuario existente
    def test_eliminar_existente(self):
        agregarUsuario("test_eliminar0","test_eliminar0","nombre4","apellido4","cosecha1",0)
        usuario = test_db.session.query(Usuario).filter_by(username = "test_eliminar0").first()
        self.assertEqual(usuario.username,"test_eliminar0")
        eliminarUsuario(usuario.id)
        usuarioDB = test_db.session.query(Usuario).filter_by(username = "test_eliminar0").first()
        self.assertIsNone(usuarioDB)
    
    # Prueba eliminar usuario no existente
    def test_eliminar_no_existente(self):
        self.assertIsNone(eliminarUsuario(99999))
    
    # Prueba editar sin id
    def test_editar_sin_id(self):
        self.assertIsNone(editarUsuario(password="prueba_eliminar"))

    # Prueba editar usuario existente
    # Se agrega un usuario y se modifica su username
    def test_editar_existente(self):
        agregarUsuario("test_editar0","test_editar0","nombre4","apellido4","cosecha",0)
        usuario = test_db.session.query(Usuario).filter_by(username = "test_editar0").first()
        self.assertEqual(usuario.username,"test_editar0")
        editarUsuario(usuario.id,username="nuevoUsername")
        usuarioDB = test_db.session.query(Usuario).filter_by(username = "nuevoUsername").first()
        self.assertEqual(usuarioDB.username,"nuevoUsername")
    
    # Prueba editar usuario no existente
    def test_eliminar_no_existente(self):
        self.assertIsNone(editarUsuario(99999,password="prueba_eliminar"))

class TestProductor(unittest.TestCase):

    def test_agregar_sin_direccion(self):
        self.assertIsNone(agregarProductor(id=12345, nombres="pepe",apellidos="perez",telefonoCelular="1234",telefonoLocal="1234",tipo=1))

    def test_agregar_sin_telefonos(self):
        self.assertIsNone(agregarProductor(id=12345, nombres="pepe",apellidos="perez",direccion="caracas",tipo=1))

    def test_agregar_sin_nombre(self):
        self.assertIsNone(agregarProductor(id=12345,apellidos="perez",telefonoCelular="1234",telefonoLocal="1234",direccion="caracas",tipo=1))
    
    def test_agregar_sin_apellidos(self):
        self.assertIsNone(agregarProductor(id=12345, nombres="pepe",telefonoCelular="1234",telefonoLocal="1234",direccion="caracas",tipo=1))

    def test_agregar_sin_tipo(self):
        self.assertIsNone(agregarProductor(id=12345, nombres="pepe",apellidos="perez",telefonoCelular="1234",telefonoLocal="1234",direccion="caracas"))

    def test_agregar_sin_id(self):
        self.assertIsNone(agregarProductor(nombres="pepe",apellidos="perez",telefonoCelular="1234",telefonoLocal="1234",direccion="caracas",tipo=1))

    def test_agregar0(self):
        agregarProductor(12345,"test0","test0","1234","1234","caracas",0)
        productorDB = test_db.session.query(Productor).filter_by(id = 12345).first()
        self.assertEqual(12345 , productorDB.id)
    
    # Prueba eliminar usuario sin suministrar id
    def test_eliminar_sin_id(self):
        self.assertIsNone(eliminarProductor())
    
    # Prueba eliminar usuario existente
    def test_eliminar_existente(self):
        agregarProductor(123456,"test_eliminar0","test_eliminar0","1234","1234","caracas",0)
        prod = test_db.session.query(Productor).filter_by(id = 123456).first()
        self.assertEqual(prod.id,123456)
        eliminarProductor(prod.id)
        productorDB = test_db.session.query(Productor).filter_by(id = 123456).first()
        self.assertIsNone(productorDB)
    
    # Prueba eliminar usuario no existente
    def test_eliminar_no_existente(self):
        self.assertIsNone(eliminarProductor(99999))
    
    # Prueba editar sin suministrar id
    def test_editar_sin_id(self):
        self.assertIsNone(editarProductor(nombres="prueba_eliminar"))

    # Prueba editar usuario existente
    # Se agrega un usuario y se modifica su username
    def test_editar_existente(self):
        agregarProductor(1234567,"test_editar0","test_editar0","1234","1234","caracas",0)
        prod = test_db.session.query(Productor).filter_by(id = 1234567).first()
        self.assertEqual(prod.id,1234567)
        editarProductor(prod.id,direccion="valencia")
        productorDB = test_db.session.query(Productor).filter_by(id = 1234567).first()
        self.assertEqual(productorDB.direccion,"valencia")
    
    # Prueba editar usuario no existente
    def test_eliminar_no_existente(self):
        self.assertIsNone(editarProductor(99999,direccion="prueba_eliminar"))

class TestTipoProductor(unittest.TestCase):

    def test_agregar_sin_descripcion(self):
        self.assertIsNone(agregarTipoProductor())

    def test_agregar0(self):
        agregarTipoProductor("vendedor1")
        tipo_productor = test_db.session.query(TipoProductor).filter_by(descripcion = "vendedor1").first()
        self.assertEqual("vendedor1" , tipo_productor.descripcion)
    
    # Prueba eliminar sin suministrar id
    def test_eliminar_sin_id(self):
        self.assertIsNone(eliminarTipoProductor())
    
    # Prueba eliminar existente
    def test_eliminar_existente(self):
        agregarTipoProductor("revendedor2")
        prod = test_db.session.query(TipoProductor).filter_by(descripcion = "revendedor2").first()
        self.assertEqual(prod.descripcion,"revendedor2")
        eliminarTipoProductor(prod.id)
        productor = test_db.session.query(TipoProductor).filter_by(descripcion = "revendedor2").first()
        print(productor)
        self.assertIsNone(productor)
    
    # Prueba eliminar no existente
    def test_eliminar_no_existente(self):
        self.assertIsNone(eliminarTipoProductor(99999))
    
    def test_eliminar_con_productor_asociado(self):
        agregarTipoProductor("revendedor1")
        tipo = test_db.session.query(TipoProductor).filter_by(descripcion = "revendedor1").first()
        agregarProductor(10,"pedro","perez","1234","1234","caracas",tipo.id)
        self.assertIsNone(eliminarTipoProductor(tipo.id))
        eliminarProductor(10)
    
    # Prueba editar no existente
    def test_editar_sin_id(self):
        self.assertIsNone(editarTipoProductor(descripcion="prueba_eliminar"))

    # Prueba editar existente
    def test_editar_existente(self):
        agregarTipoProductor("vendedor3")
        prod = test_db.session.query(TipoProductor).filter_by(descripcion = "vendedor3").first()
        self.assertEqual(prod.descripcion,"vendedor3")
        editarTipoProductor(prod.id,descripcion="vendedor3")
        productorDB = test_db.session.query(TipoProductor).filter_by(descripcion = "vendedor3").first()
        self.assertEqual(productorDB.descripcion,"vendedor3")
    
    # Prueba editar usuario no existente
    def test_eliminar_no_existente(self):
        self.assertIsNone(editarTipoProductor(99999,descripcion="prueba_eliminar"))

  

if __name__ == '__main__':
    test_db.Base.metadata.create_all(test_db.engine)
    unittest.main()
