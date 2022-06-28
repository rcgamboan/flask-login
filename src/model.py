import database as db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

class Usuario(db.Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement = True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    cosecha = Column(String, nullable=False)
    rol = Column(Integer, default=0, nullable=False)
    # rol = 0 -> Usuario normal
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

class Productor(db.Base):
    __tablename__ = 'productor'
    id = Column(Integer, primary_key=True)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    telefonoCelular = Column(String, nullable=False)
    telefonoLocal = Column(String, nullable=True)
    direccion = Column(String, nullable=False)
    tipo = Column(Integer, ForeignKey("tipoproductor.id"))

    def __init__(self, id, nombres,apellidos,telefonoCelular,telefonoLocal,direccion,tipo):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefonoCelular = telefonoCelular
        self.telefonoLocal = telefonoLocal
        self.direccion = direccion
        self.tipo = tipo

    def __repr__(self):
        return f'Productor({self.nombres}, {self.apellidos}, {self.tipo})'
    def __str__(self):
        return self.nombres

class TipoProductor(db.Base):
    __tablename__ = 'tipoproductor'
    id = Column(Integer, primary_key=True, autoincrement = True)
    direccion = Column(String, nullable=False)
    productor = relationship("Productor")

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        return f'TipoProductor({self.descripcion})'
    def __str__(self):
        return self.descripcion