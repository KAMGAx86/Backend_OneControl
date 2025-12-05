from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Body,Depends,HTTPException
from classes import PlayerValidation, Token
from database import db_dependancy
from models import Players
from  starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError 



router = APIRouter(
    tags=["auth"],

    prefix="/auth"
)



oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto") 

JWT_SECRET_KEY = "f10f9e1b3f0a198271bd43a07f79eb1a7cc36b4fb90f594aeeca89a0f7ebe79f6502a9bad74267558224052c36411b4d22b5f053e4f7d34b1ed893b92c3a940b"

JWT_ALGO = "HS256"


def authenticate_player(username: str,password: str,db):
    found_player = db.query(Players).filter(Players.username == username).first()
    if not found_player:
        return False
    if not bcrypt_context.verify(password,found_player.hashed_password): 
        return False
    return found_player

def create_token(username: str,user_id: int,expire_delta: timedelta):
    encoded_data = {"sub":username,"id":user_id}

    expiration = datetime.now(timezone.utc) + expire_delta
    encoded_data.update({"expi": expiration.timestamp() })

    return jwt.encode(encoded_data, JWT_SECRET_KEY, JWT_ALGO)

import jwt
from fastapi import status, HTTPException, Depends 
from typing import Annotated
from jose import JWTError

async def get_current_player(token: Annotated[str, Depends(oauth2_bearer)]):


    try:
        
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,  
            algorithms=JWT_ALGO 
        )

        username: str = payload.get("sub")

        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="wrong credentials" 
            )

        return {"username": username, "id": user_id}

    
     
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="wrong credentials"  
        )



@router.post("/login",response_model=Token,status_code=status.HTTP_200_OK)
async def login_player(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], db: db_dependancy):
    player_authenticated = authenticate_player(form_data.username,form_data.password,db)

    if not player_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="wrong credentials")

    token = create_token(player_authenticated.username,player_authenticated.id,timedelta(minutes=30))
    return {"access_token":token,"token_type": "Bearer"}
    # return form_data.password
