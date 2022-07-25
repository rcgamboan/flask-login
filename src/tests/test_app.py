import datetime
import unittest
import test_database as test_db
from test_usuario import agregarUsuario, editarUsuario, login, eliminarUsuario
from test_recolector import editarRecolector, agregarRecolector, eliminarRecolector
from test_tipo_recolector import editarTipoRecolector, agregarTipoRecolector, eliminarTipoRecolector
from test_model import Usuario, Recolector, TipoRecolector, Cosecha, Compra, Evento
from test_cosecha import agregarCosecha, activarCosecha, editarCosecha
from test_compra import generarCompra
from test_evento import eliminarEvento, agregarEvento


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
        agregarCosecha("prueba")
        agregarUsuario("rgcn","rgcn","nombre","apellido",0,1,)
        self.assertIsNotNone( login("rgcn","rgcn"))
    
    def test_login2(self):
        agregarCosecha("prueba1")
        agregarUsuario("prueba2","prueba2","nombre2","apellido2",0,0)
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
        agregarCosecha("prueba1")
        agregarUsuario("test0","test0","nombre4","apellido4",0,0)
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

class TestRecolector(unittest.TestCase):

    def test_agregar_sin_direccion(self):
        self.assertIsNone(agregarRecolector(id=12345, nombres="pepe",apellidos="perez",telefonoCelular="1234",telefonoLocal="1234",tipo=1))

    def test_agregar_sin_telefonos(self):
        self.assertIsNone(agregarRecolector(id=12345, nombres="pepe",apellidos="perez",direccion="caracas",tipo=1))

    def test_agregar_sin_nombre(self):
        self.assertIsNone(agregarRecolector(id=12345,apellidos="perez",telefonoCelular="1234",telefonoLocal="1234",direccion="caracas",tipo=1))
    
    def test_agregar_sin_apellidos(self):
        self.assertIsNone(agregarRecolector(id=12345, nombres="pepe",telefonoCelular="1234",telefonoLocal="1234",direccion="caracas",tipo=1))

    def test_agregar_sin_tipo(self):
        self.assertIsNone(agregarRecolector(id=12345, nombres="pepe",apellidos="perez",telefonoCelular="1234",telefonoLocal="1234",direccion="caracas"))

    def test_agregar_sin_id(self):
        self.assertIsNone(agregarRecolector(nombres="pepe",apellidos="perez",telefonoCelular="1234",telefonoLocal="1234",direccion="caracas",tipo=1))

    def test_agregar0(self):
        agregarRecolector(12345,"test0","test0","1234","1234","caracas","valencia",0)
        RecolectorDB = test_db.session.query(Recolector).filter_by(id = 12345).first()
        self.assertEqual(12345 , RecolectorDB.id)
    
    # Prueba eliminar usuario sin suministrar id
    def test_eliminar_sin_id(self):
        self.assertIsNone(eliminarRecolector())
    
    # Prueba eliminar usuario existente
    def test_eliminar_existente(self):
        agregarRecolector(123456,"test_eliminar0","test_eliminar0","1234","1234","caracas","valencia",0)
        prod = test_db.session.query(Recolector).filter_by(id = 123456).first()
        self.assertEqual(prod.id,123456)
        eliminarRecolector(prod.id)
        RecolectorDB = test_db.session.query(Recolector).filter_by(id = 123456).first()
        self.assertIsNone(RecolectorDB)
    
    # Prueba eliminar usuario no existente
    def test_eliminar_no_existente(self):
        self.assertIsNone(eliminarRecolector(99999))
    
    # Prueba editar sin suministrar id
    def test_editar_sin_id(self):
        self.assertIsNone(editarRecolector(nombres="prueba_eliminar"))

    # Prueba editar usuario existente
    # Se agrega un usuario y se modifica su username
    def test_editar_existente(self):
        agregarRecolector(1234567,"test_editar0","test_editar0","1234","1234","caracas","valencia",0)
        prod = test_db.session.query(Recolector).filter_by(id = 1234567).first()
        self.assertEqual(prod.id,1234567)
        editarRecolector(prod.id,direccion="valencia")
        RecolectorDB = test_db.session.query(Recolector).filter_by(id = 1234567).first()
        self.assertEqual(RecolectorDB.direccion,"valencia")
    
    # Prueba editar usuario no existente
    def test_eliminar_no_existente(self):
        self.assertIsNone(editarRecolector(99999,direccion="prueba_eliminar"))
    
    def test_editar_sin_id(self):
        self.assertIsNone(editarCosecha())

class TestTipoRecolector(unittest.TestCase):

    def test_agregar_sin_descripcion(self):
        self.assertIsNone(agregarTipoRecolector())

    def test_agregar0(self):
        agregarTipoRecolector("vendedor1")
        tipo_Recolector = test_db.session.query(TipoRecolector).filter_by(direccion = "vendedor1").first()
        self.assertEqual("vendedor1" , tipo_Recolector.direccion)
    
    # Prueba eliminar sin suministrar id
    def test_eliminar_sin_id(self):
        self.assertIsNone(eliminarTipoRecolector())
    
    # Prueba eliminar existente
    def test_eliminar_existente(self):
        agregarTipoRecolector("revendedor2")
        prod = test_db.session.query(TipoRecolector).filter_by(direccion = "revendedor2").first()
        self.assertEqual(prod.direccion,"revendedor2")
        eliminarTipoRecolector(prod.id)
        Recolector = test_db.session.query(TipoRecolector).filter_by(direccion = "revendedor2").first()
        self.assertIsNone(Recolector)
    
    # Prueba eliminar no existente
    def test_eliminar_no_existente(self):
        self.assertIsNone(eliminarTipoRecolector(99999))
    
    def test_eliminar_con_Recolector_asociado(self):
        agregarTipoRecolector("revendedor1")
        tipo = test_db.session.query(TipoRecolector).filter_by(direccion = "revendedor1").first()
        agregarRecolector(10,"pedro","perez","1234","1234","caracas",tipo.id)
        self.assertIsNone(eliminarTipoRecolector(tipo.id))
        eliminarRecolector(10)
    
    # Prueba editar no existente
    def test_editar_sin_id(self):
        self.assertIsNone(editarTipoRecolector(direccion="prueba_eliminar"))

    # Prueba editar existente
    def test_editar_existente(self):
        agregarTipoRecolector("vendedor3")
        prod = test_db.session.query(TipoRecolector).filter_by(direccion = "vendedor3").first()
        self.assertEqual(prod.direccion,"vendedor3")
        editarTipoRecolector(prod.id,direccion="vendedor3")
        RecolectorDB = test_db.session.query(TipoRecolector).filter_by(direccion = "vendedor3").first()
        self.assertEqual(RecolectorDB.direccion,"vendedor3")
    
    # Prueba editar usuario no existente
    def test_eliminar_no_existente(self):
        self.assertIsNone(editarTipoRecolector(99999,direccion="prueba_eliminar"))

class TestCosecha(unittest.TestCase):

    def test_agregar_sin_descripcion(self):
        self.assertIsNone(agregarCosecha())

    def test_agregar0(self):
        agregarCosecha("prueba3")
        cosecha = test_db.session.query(Cosecha).filter_by(descripcion = "prueba3").first()
        self.assertEqual("prueba3" , cosecha.descripcion)
    
    def test_agregar_existente(self):
        agregarCosecha("prueba3")
        self.assertIsNone(agregarCosecha("prueba3"))
    
    def test_editar_sin_id(self):
        agregarCosecha("prueba4")
        self.assertIsNone(editarCosecha())

    def test_editar_existente(self):
        agregarCosecha("prueba4")
        prod = test_db.session.query(Cosecha).filter_by(descripcion = "prueba4").first()
        editarCosecha(id=prod.id,descripcion="prueba5")
        RecolectorDB = test_db.session.query(Cosecha).filter_by(descripcion="prueba5").first()
        self.assertEqual(RecolectorDB.descripcion,"prueba5")
    
    def test_activar_sin_id(self):
        
        self.assertIsNone(activarCosecha())
    
    def test_activar_cosecha(self):
        agregarCosecha("prueba5")
        cosecha = test_db.session.query(Cosecha).filter_by(descripcion = "prueba5").first()
        activarCosecha(cosecha.id)
        self.assertEqual(0,cosecha.activa)
        activarCosecha(cosecha.id)
        self.assertEqual(1,cosecha.activa)
    
class TestCompra(unittest.TestCase):

    def test_generar_compra(self):
        agregarTipoRecolector("prueba1")
        agregarRecolector(9999,"pedro","perez","1234","1234","caracas","valencia",0)
        generarCompra(datetime.datetime.now(),999,0,0,"","","","","",1)
        self.assertIsNotNone( test_db.session.query(Compra).filter_by(cedula = 999).first())
    
    def test_generar_compra_sin_cedula(self):
        agregarTipoRecolector("prueba2")
        agregarRecolector(9899,"pedro","perez","1234","1234","caracas","valencia",0)
        generarCompra(fecha=datetime.datetime.now(), 
                    tipo="",
                    precio=-1,
                    cacao="",
                    cantidad="",
                    cosecha=-1,
                    observaciones="",
                    humedad="",
                    merma=0)
        self.assertIsNone( test_db.session.query(Compra).filter_by(cedula = 9899).first())

class TestEvento(unittest.TestCase):

    def test_agregar_evento_sin_usuario(self):
        self.assertIsNone( agregarEvento(descripcion="",modulo="",fecha=""))
    
    def test_agregar_evento_sin_descripcion(self):
        self.assertIsNone( agregarEvento(usuario="",modulo="",fecha=""))
    
    def test_evento_agregar_compra(self):
        agregarTipoRecolector("prueba1")
        agregarRecolector(9999,"pedro","perez","1234","1234","caracas","valencia",0)
        generarCompra(datetime.datetime.now(),999,0,0,"","","","","",1)
        agregarEvento(0,"Agregar","Compra",datetime.datetime.now())
        self.assertIsNotNone( test_db.session.query(Evento).filter_by(usuario =0).first())
    
    def test_evento_agregar_usuario(self):
        agregarCosecha("prueba1")
        agregarUsuario("test0","test0","nombre4","apellido4",0,0)
        usuarioDB = test_db.session.query(Usuario).filter_by(username = "test0").first()
        agregarEvento(usuarioDB.id,"Agregar","Usuario",datetime.datetime.now())
        self.assertIsNotNone( test_db.session.query(Evento).filter_by(usuario=usuarioDB.id).first())
    
    def test_evento_eliminar_usuario(self):
        agregarCosecha("prueba1")
        agregarUsuario("test2","test2","nombre4","apellido4",0,0)
        usuarioDB = test_db.session.query(Usuario).filter_by(username = "test2").first()
        agregarEvento(usuarioDB.id,"Eliminar","Usuario",datetime.datetime.now())
        eliminarUsuario(usuarioDB.id)
        self.assertIsNotNone( test_db.session.query(Evento).filter_by(usuario=usuarioDB.id).first())
    
    def test_evento_agregar_recolector(self):
        agregarRecolector(12345,"test0","test0","1234","1234","caracas","valencia",0)
        RecolectorDB = test_db.session.query(Recolector).filter_by(id = 12345).first()
        agregarEvento(RecolectorDB.id,"Agregar","Recolector",datetime.datetime.now())
        self.assertIsNotNone( test_db.session.query(Evento).filter_by(usuario=RecolectorDB.id).first())
    
    def test_evento_eliminar_recolector(self):
        agregarRecolector(125,"test0","test0","1234","1234","caracas","valencia",0)
        RecolectorDB = test_db.session.query(Recolector).filter_by(id = 125).first()
        agregarEvento(RecolectorDB.id,"Eliminar","Recolector",datetime.datetime.now())
        eliminarRecolector(RecolectorDB.id)
        self.assertIsNotNone( test_db.session.query(Evento).filter_by(usuario=RecolectorDB.id).first())
    
    def test_evento_agregar_tipo(self):
        agregarTipoRecolector("vendedor1")
        tipo_Recolector = test_db.session.query(TipoRecolector).filter_by(direccion = "vendedor1").first()
        agregarEvento(tipo_Recolector.id,"Agregar","Tipo de Recolector",datetime.datetime.now())
        self.assertIsNotNone( test_db.session.query(Evento).filter_by(usuario=tipo_Recolector.id).first())
    
    def test_evento_eliminar_tipo(self):
        agregarTipoRecolector("vendedor4")
        tipo_Recolector = test_db.session.query(TipoRecolector).filter_by(direccion = "vendedor1").first()
        agregarEvento(tipo_Recolector.id,"Eliminar","Tipo de Recolector",datetime.datetime.now())
        eliminarTipoRecolector(tipo_Recolector.id)
        self.assertIsNotNone( test_db.session.query(Evento).filter_by(usuario=tipo_Recolector.id).first())

if __name__ == '__main__':
    test_db.Base.metadata.create_all(test_db.engine)
    unittest.main()
