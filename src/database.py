from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Inicializando el engine de SQLAlchemy para poder crear y manejar la BD
engine = create_engine('sqlite:///usuarios.sqlite?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()