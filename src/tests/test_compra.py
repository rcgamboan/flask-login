import datetime
from test_model import Compra, Recolector, TipoRecolector
import test_database as test_db

def generarCompra(fecha=datetime.datetime.now(), cedula="",tipo="",precio=-1,cacao="",cantidad="",humedad=""):
    if cedula == "" or tipo == "":
        return None

    #recolector = test_db.session.query(Recolector).filter_by(id=cedula).first()
    #tipo_rec = test_db.session.query(TipoRecolector).filter_by(id=tipo).first()
    #if cantidad > recolector.cantidad:
    #   return None
    #else:    
    compra = Compra(fecha, cedula,tipo,precio,cacao,cantidad,humedad)
    test_db.session.add(compra)
    #recolector.cantidad -= cantidad
    test_db.session.commit()