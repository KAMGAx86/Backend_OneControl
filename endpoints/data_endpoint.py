
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,Body
from database import db_dependancy
from sqlalchemy import text
from starlette import status
from endpoints.auth_endpoint import get_current_user
from models import User
from comparative_ca import result

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
    return result

