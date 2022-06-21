import database as db
from sqlalchemy import Column, Integer, String, Float

class Usuario(db.Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    rol = Column(Integer, default=0, nullable=False)
    # rol = 0 -> Usuario normal
    # rol = 1 -> admin
    # rol = 2 -> proveedor

    def __init__(self, username, password, rol = 0):
        self.username = username
        self.password = password
        self.rol = rol

    def __repr__(self):
        return f'Usuario({self.username}, {self.password}, {self.rol})'
    def __str__(self):
        return self.username

class Producto(db.Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    proveedor = Column(Integer)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=True)
    precio = Column(Integer, default=0, nullable=False)


    def __init__(self, nombre, proveedor, precio, descripcion = ''):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.proveedor = proveedor

    def __repr__(self):
        return f'Producto({self.nombre}, {self.descripcion}, {self.precio})'
    def __str__(self):
        return self.nombre