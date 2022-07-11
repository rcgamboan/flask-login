from test_model import TipoRecolector, Recolector
from werkzeug.security import  generate_password_hash
import test_database as test_db

def editarTipoRecolector(id = -1,direccion="",precio=0):

    if id == -1 or id == None:
        return None
    
    logged_user = test_db.session.query(TipoRecolector).filter_by(id = id).first()
    
    if logged_user != None:

        prod = test_db.session.query(TipoRecolector).filter_by(id = id).first()
        if direccion != "" and direccion != None:
            prod.direccion = direccion
        
        if precio != 0 and precio != None:
            prod.precio = precio

        test_db.session.commit()
    else:
        return None

def eliminarTipoRecolector(id=-1):

    if id == -1:
        return None
    
    prod = test_db.session.query(Recolector).filter_by(tipo = id).all()
    if len(prod) > 0:
        return None
    else:
        logged_user = test_db.session.query(TipoRecolector).filter_by(id = id).first()
        if logged_user != None:
            user = test_db.session.query(TipoRecolector).get(id)
            test_db.session.delete(user)
            test_db.session.commit()
        else:
            return None

def agregarTipoRecolector(direccion = "",precio=0):

    if direccion == "":
        return None
    
    logged_user = test_db.session.query(TipoRecolector).filter_by(direccion = direccion).first()
    
    if logged_user == None:
        prod = TipoRecolector(direccion,precio)
        test_db.session.add(prod)
        test_db.session.commit()
    else:
        return None
