from werkzeug.security import check_password_hash , generate_password_hash
from test_model import Usuario
import test_database as test_db

def editarUsuario(id = -1,username = "", password = "",nombres = "",apellidos = "",cosecha = "",rol = -1):

    if id == -1 or id == None:
        return None
    
    logged_user = test_db.session.query(Usuario).filter_by(id = id).first()
    
    if logged_user != None:
        user = test_db.session.query(Usuario).filter_by(id = id).first()
        if username != "" and username != None:
            user.username = username
        
        if password != "" and password != None:
            user.password = generate_password_hash(password)

        if nombres != "" and nombres != None:            
            user.nombres = nombres

        if apellidos != "" and apellidos != None:
            user.apellidos = apellidos
        
        if cosecha != "" and cosecha != None:
            user.cosecha = cosecha
        
        if rol != -1 and rol != None:
            user.rol = rol

        test_db.session.commit()
    else:
        return None

def eliminarUsuario(id=-1):

    if id == -1:
        return None

    logged_user = test_db.session.query(Usuario).filter_by(id = id).first()
    if logged_user != None:
        user = test_db.session.query(Usuario).get(id)
        test_db.session.delete(user)
        test_db.session.commit()
    else:
        return None

def agregarUsuario(username="",password="",nombres="",apellidos="",cosecha="",rol=-1):

    if username == "" or password == "" or cosecha == "" or nombres == "" or apellidos == "":
        return None
    
    if rol == -1:
        return None
    

    logged_user = test_db.session.query(Usuario).filter_by(username = username).first()
    
    if logged_user == None:
        user = Usuario(username, generate_password_hash(password),nombres,apellidos,cosecha,rol)
        test_db.session.add(user)
        test_db.session.commit()
    else:
        return None

def login(user="",password=""):

    if user == "" or password == "":
        return None

    
    logged_user = test_db.session.query(Usuario).filter_by(username = user).first()
    if logged_user != None:

        if check_password_hash(logged_user.password,password):

            if logged_user.rol == 0:
                string = "Se ha iniciado sesion como usuario normal!"
                return string
            else:
                string = "Se ha iniciado sesion como administrador!"
                return string
        else:
            string = "Alguno de los datos es incorrecto"
            return string
    else:
        return None
  