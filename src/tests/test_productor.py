from test_model import Productor
from werkzeug.security import generate_password_hash
import test_database as test_db

def editarProductor(id=-1, nombres="",apellidos="",telefonoCelular="",telefonoLocal="",direccion="",tipo=-1):

    if id == -1 or id == None:
        return None
    
    logged_user = test_db.session.query(Productor).filter_by(id = id).first()
    
    if logged_user != None:

        prod = test_db.session.query(Productor).filter_by(id = id).first()
        if nombres != "" and nombres != None:
            prod.nombres = nombres
        
        if apellidos != "" and apellidos != None:
            prod.apellidos = apellidos

        if telefonoCelular != "" and telefonoCelular != None:            
            prod.telefonoCelular = telefonoCelular

        if telefonoLocal != "" and telefonoLocal != None:
            prod.telefonoLocal = telefonoLocal
        
        if direccion != "" and direccion != None:
            prod.direccion = direccion
        
        if tipo != -1 and tipo != None:
            prod.tipo = tipo

        test_db.session.commit()
    else:
        return None

def eliminarProductor(id=-1):

    if id == -1:
        return None

    logged_user = test_db.session.query(Productor).filter_by(id = id).first()
    if logged_user != None:
        prod = test_db.session.query(Productor).get(id)
        test_db.session.delete(prod)
        test_db.session.commit()
    else:
        return None

def agregarProductor(id=-1, nombres="",apellidos="",telefonoCelular="",telefonoLocal="",direccion="",tipo=-1):

    if id == -1:
        return None

    if nombres == "" or apellidos == "" or telefonoCelular == "" or telefonoLocal == "" or direccion == "":
        return None
    
    if tipo == -1:
        return None
    

    logged_user = test_db.session.query(Productor).filter_by(id = id).first()
    
    if logged_user == None:
        prod = Productor(id, nombres,apellidos,telefonoCelular,telefonoLocal,direccion,tipo)
        test_db.session.add(prod)
        test_db.session.commit()
    else:
        return None
