
from fastapi import APIRouter, Depends, HTTPException,Body
from database import db_dependancy
from sqlalchemy import text
from starlette import status
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
    