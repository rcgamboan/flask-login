import test_database as db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
import datetime

class Usuario(db.Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement = True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    cosecha = Column(Integer, ForeignKey("cosecha.id"))
    rol = Column(Integer, default=0, nullable=False)
    # rol = 0 -> analista
    # rol = 1 -> admin
    # rol = 2 -> productor

    def __init__(self,username, password, nombres,apellidos,cosecha,rol = 0):
        self.username = username
        self.password = password
        self.nombres = nombres
        self.apellidos = apellidos
        self.cosecha = cosecha
        self.rol = rol

    def __repr__(self):
        return f'Usuario({self.username}, {self.password}, {self.rol})'
    def __str__(self):
        return self.username

class Recolector(db.Base):
    __tablename__ = 'recolector'
    id = Column(Integer, primary_key=True)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    telefonoCelular = Column(String, nullable=False)
    telefonoLocal = Column(String, nullable=True)
    direccion = Column(String, nullable=False)
    direccion2 = Column(String, nullable=True)
    tipo = Column(Integer, ForeignKey("tiporecolector.id"))
    cantidad = Column(Integer, nullable=True)

    def __init__(self, id, nombres,apellidos,telefonoCelular,telefonoLocal,direccion,direccion2,tipo):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefonoCelular = telefonoCelular
        self.telefonoLocal = telefonoLocal
        self.direccion = direccion
        self.direccion2 = direccion2
        self.tipo = tipo

    def __repr__(self):
        return f'Recolector({self.nombres}, {self.apellidos}, {self.tipo})'
    def __str__(self):
        return self.nombres

class TipoRecolector(db.Base):
    __tablename__ = 'tiporecolector'
    id = Column(Integer, primary_key=True, autoincrement = True)
    direccion = Column(String, nullable=False)
    precio = Column(Integer, nullable=False)
    recolector = relationship("Recolector")
    precioProd = relationship("Compra")

    def __init__(self, direccion,precio):
        self.direccion= direccion
        self.precio= precio

    def __repr__(self):
        return f'TipoRecolector({self.direccion})'
    def __str__(self):
        return self.direccion

class Cosecha(db.Base):
    __tablename__ = 'cosecha'
    id = Column(Integer, primary_key=True, autoincrement = True)
    descripcion = Column(String, nullable=False)
    inicio = Column(Date, default=datetime.datetime.now())
    fin = Column(Date, default=datetime.datetime.now())
    numCosecha = relationship("Usuario")
    activa = Column(Integer, nullable = False)
    

    def __init__(self, descripcion, inicio, fin,activa=1):
        self.descripcion= descripcion
        self.inicio = inicio
        self.fin = fin
        self.activa = activa
        
    # activa : 1 -> activa
    #          0 -> inactiva

    def __repr__(self):
        return f'Cosecha({self.descripcion,self.inicio,self.fin})'
    def __str__(self):
        return self.direccion

class Compra(db.Base):
    __tablename__ = 'compra'
    id = Column(Integer, primary_key=True, autoincrement = True)
    fecha = Column(Date, default=datetime.datetime.now())
    cedula = Column(Integer, ForeignKey("recolector.id"))
    tipo = Column(Integer, ForeignKey("tiporecolector.id"))
    precio = Column(Integer, default=0)
    cacao = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    monto = Column(Integer, nullable=False)
    cosecha = Column(Integer, ForeignKey("cosecha.id"))
    humedad = Column(Integer, nullable=False)
    observaciones = Column(String, nullable=True)
    merma = Column(Integer, nullable=False)


    def __init__(self, fecha, cedula,tipo,precio,cacao,cantidad,cosecha,observaciones,humedad,merma):
        self.fecha = fecha
        self.cedula = cedula
        self.monto = precio * cantidad
        self.tipo = tipo
        self.precio = precio
        self.cacao = cacao
        self.cantidad = cantidad
        self.humedad = humedad
        self.cosecha = cosecha
        self.merma = merma
        self.observaciones = observaciones

    def __repr__(self):
        return f'Compra({self.fecha,self.precio,self.cantidad})'
    def __str__(self):
        return self.fecha