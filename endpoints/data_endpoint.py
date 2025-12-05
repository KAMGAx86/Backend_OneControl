
from fastapi import APIRouter, Depends, HTTPException,Body
from database import db_dependancy
from sqlalchemy import text
from starlette import status
from pydantic_classes import UserValidation
from models import User


router = APIRouter(
    
    tags=["data_endpoint"],
    prefix="/data"
    
)

@router.get("/hearbeat")
async def heartbeat(db: db_dependancy):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "DATABASE OK"}
    except Exception as e:
        return {"error": str(e)}
    
@router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_data(db: db_dependancy,user: UserValidation = Body()):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        nom=user.nom,
        prenom=user.prenom,
        telephone=user.telephone,
        email=user.email,
        hashed_password=user.password,
        enterprise_name=user.enterprise_name,
        enterprise_address=user.enterprise_address,
        employees_number=user.employees_number,
        aproximative_ca=user.aproximative_ca,
        secteur_activite=user.secteur_activite
    )
    db.add(new_user)
    db.commit()
    