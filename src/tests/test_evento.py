from test_model import Evento
import test_database as test_db

def eliminarEvento(id=-1):

    if id == -1:
        return None

    event = test_db.session.query(Evento).filter_by(id = id).first()
    if event != None:
        test_db.session.delete(event)
        test_db.session.commit()
    else:
        return None

def agregarEvento(usuario="",descripcion="",modulo="",fecha=""):
    if usuario == "" or descripcion == "" or modulo == "" or fecha == "":
        return None
    event = Evento(usuario, descripcion,modulo, fecha)
    test_db.session.add(event)
    test_db.session.commit()