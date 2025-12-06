
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,Body, Path
from database import db_dependancy
from sqlalchemy import text
from starlette import status
from endpoints.auth_endpoint import get_current_user
from models import User
from comparative_ca import comprative_ca_r
from simulateur_lancement import resultat
from pydantic_classes import UserValidation
from simulateur_prix import resultats_simulaton_prix

router = APIRouter(
    
    tags=["data_endpoint"],
    
    prefix="/data"
    
)

user_dependency = Annotated[dict,Depends(get_current_user)]


@router.get("/hearbeat")
async def heartbeat(db: db_dependancy):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "DATABASE OK"}
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/comparattive_ca",status_code=status.HTTP_200_OK)
async def comparative_ca():
    return comprative_ca_r

@router.get("/simulateur_lancement_produit")
async def simulateur_embauche():
    return resultat

@router.get("/simulateur_prix")
async def simulateur_prix():
    return resultats_simulaton_prix


@router.get("/simulateur_embauche")
async def simulateur_lancement_produit():
    return {"ok": "fonctionnent"}


@router.delete("/delete_user/{user_email}")
async def delete_user(db: db_dependancy,user: user_dependency,user_email: str = Path()):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentification failed")
    
    user_db = db.query(User).filter(User.email == user_email).first()
    
    if user_db is None:
        raise HTTPException(status_code=404, detail="hero does not found")
    
    db.delete(user_db)
    db.commit()

@router.put("/update_user/{user_email}")
async def update_user(db: db_dependancy,user: user_dependency,user_email : str  = Path(),user_body: UserValidation = Body() ):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentification failed")
    
    user_db = db.query(User).filter(User.email == user_email).first()
    
    if user_db is None:
        raise HTTPException(status_code=404, detail="hero does not found")
    
    user_db.nom = user_body.nom
    user_db.prenom = user_body.prenom
    user_db.telephone = user_body.telephone
    user_db.hashed_password = user_body.hashed_password
    user_db.email = user_body.email
    user_db.enterprise_name = user_body.enterprise_name
    user_db.enterprise_address = user_body.enterprise_address
    user_db.employees_number = user_body.employees_number
    user_db.aproximative_ca = user_body.aproximative_ca
    
    
    
