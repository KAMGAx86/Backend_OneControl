from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base


class User(Base):
    __tablename__ = "User"
    
    id = Column(Integer,autoincrement=True,index=True,primary_key=True)
    
    nom = Column(String)
    prenom = Column(String)
    telephone = Column(String)
    hashed_password = Column(String)
    email = Column(String)
    enterprise_name = Column(String)
    enterprise_address = Column(String)
    employees_number = Column(Integer)
    aproximative_ca = Column(String)
    secteur_activite = Column(String)
    code = Column(String)
    
