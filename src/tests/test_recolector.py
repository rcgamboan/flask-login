from test_model import Recolector
from werkzeug.security import generate_password_hash
import test_database as test_db

def editarRecolector(id=-1, nombres="",apellidos="",telefonoCelular="",telefonoLocal="",direccion="",direccion2="",tipo=-1):

    if id == -1 or id == None:
        return None
    
    logged_user = test_db.session.query(Recolector).filter_by(id = id).first()
    
    if logged_user != None:

        prod = test_db.session.query(Recolector).filter_by(id = id).first()
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
        
        if direccion2 != "" and direccion2 != None:
            prod.direccion = direccion
        
        if tipo != -1 and tipo != None:
            prod.tipo = tipo

        test_db.session.commit()
    else:
        return None

def eliminarRecolector(id=-1):

    if id == -1:
        return None

    logged_user = test_db.session.query(Recolector).filter_by(id = id).first()
    if logged_user != None:
        prod = test_db.session.query(Recolector).get(id)
        test_db.session.delete(prod)
        test_db.session.commit()
    else:
        return None

def agregarRecolector(id=-1, nombres="",apellidos="",telefonoCelular="",telefonoLocal="",direccion="",direccion2="",tipo=-1):

    if id == -1:
        return None

    if nombres == "" or apellidos == "" or telefonoCelular == "" or telefonoLocal == "" or direccion == "":
        return None
    
    if tipo == -1:
        return None
    

    logged_user = test_db.session.query(Recolector).filter_by(id = id).first()
    
    if logged_user == None:
        prod = Recolector(id, nombres,apellidos,telefonoCelular,telefonoLocal,direccion,direccion2,tipo)
        test_db.session.add(prod)
        test_db.session.commit()
    else:
        return None
