import datetime
from test_model import Cosecha
import test_database as test_db

def agregarCosecha(descripcion="", inicio = datetime.datetime.now(), fin = datetime.datetime.now(),activa = 1):
    db = test_db.session.query(Cosecha).filter_by(descripcion = descripcion).first()

    if descripcion == "":
        return None

    if db:
        return None
    else:
        cosecha = Cosecha(descripcion,inicio,fin,activa)
        test_db.session.add(cosecha)
        test_db.session.commit()

def editarCosecha(id=-1,descripcion = "", inicio = "", fin = "", activa=-1):

    if id == -1:
        return None
    cosecha = test_db.session.query(Cosecha).filter_by(id = id).first()
    
    if cosecha != None:
        
        if descripcion != "" and descripcion != None:            
            cosecha.descripcion = descripcion
        
        if inicio != "" and inicio != None:            
            cosecha.inicio = inicio
        
        if fin != "" and fin != None:            
            cosecha.fin = fin
        
        if activa != -1 and activa != None:            
            cosecha.activa = activa


        test_db.session.commit()
    else:
        return None


def activarCosecha(id):
    cosecha = test_db.session.query(Cosecha).filter_by(id=id).first()
    if cosecha.activa == 1:

        cosecha.activa = 0
    else:
        cosecha.activa = 0
    test_db.session.commit()
