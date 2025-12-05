from fastapi import Depends
from sqlalchemy  import create_engine
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated


#URL de connexion a la base de donner
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/ONECONTROLDB"

#creation du moteur de connexion a la base de donner
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# defnition de la seesionlocal (autoflush=False pour ne pas valider automatiquement les transactions,autocommit=False pour ne pas commiter automatiquement les transactions) (bind=engin pour lier la session a l'engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#definition de la base comme modele parent a utiliser par tous les models de table
Base = declarative_base()

#fonction de connexion ala base de donner que  on va devleper dans les routes pour chaque requete

#DEPENDENCY CORE
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#untiliser la dependancy core dans une dependancy annotation
db_dependancy = Annotated[Session, Depends(get_db)]