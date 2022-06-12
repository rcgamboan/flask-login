import database as db
from sqlalchemy import Column, Integer, String, Float

class Usuario(db.Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String)
    isAdmin = Column(Integer, default=0)


    def __init__(self, username, password, isAdmin = 0):
        self.username = username
        self.password = password
        self.isAdmin = isAdmin

    def __repr__(self):
        return f'Usuario({self.username}, {self.password}, {self.isAdmin})'
    def __str__(self):
        return self.username