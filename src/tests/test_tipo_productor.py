from test_model import TipoProductor, Productor
from werkzeug.security import  generate_password_hash
import test_database as test_db

def editarTipoProductor(id = -1,descripcion = ""):

    if id == -1 or id == None:
        return None
    
    logged_user = test_db.session.query(TipoProductor).filter_by(id = id).first()
    
    if logged_user != None:

        prod = test_db.session.query(TipoProductor).filter_by(id = id).first()
        if descripcion != "" and descripcion != None:
            prod.descripcion = descripcion

        test_db.session.commit()
    else:
        return None

def eliminarTipoProductor(id=-1):

    if id == -1:
        return None
    
    prod = test_db.session.query(Productor).filter_by(tipo = id).all()
    if len(prod) > 0:
        return None
    else:
        logged_user = test_db.session.query(TipoProductor).filter_by(id = id).first()
        if logged_user != None:
            user = test_db.session.query(TipoProductor).get(id)
            test_db.session.delete(user)
            test_db.session.commit()
        else:
            return None

def agregarTipoProductor(descripcion = ""):

    if descripcion == "":
        return None
    
    logged_user = test_db.session.query(TipoProductor).filter_by(descripcion = descripcion).first()
    
    if logged_user == None:
        prod = TipoProductor(descripcion)
        test_db.session.add(prod)
        test_db.session.commit()
    else:
        return None
