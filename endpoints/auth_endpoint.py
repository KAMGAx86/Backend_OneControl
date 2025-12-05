from models import User
from pydantic_classes import UserValidation
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Body,Depends,HTTPException
from pydantic_classes import Token
from database import db_dependancy
from  starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer #permet de creer un petit formulaire de login pour tester l'autentifucation
from jose import jwt,JWTError # pour creer des cles de token

router = APIRouter(
    tags=["auth_endpoint"],
    
    prefix="/auth"
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET_KEY =  "f10f9e1b3f0a198271bd43a07f79eb1a7cc36b4fb90f594aeeca89a0f7ebe79f6502a9bad74267558224052c36411b4d22b5f053e4f7d34b1ed893b92c3a940b"

JWT_ALGO = "HS256"

# HELPER FUNCTION FOR LOGIN

#fonction de login qui permet de tester les infos utilisateur
def authenticate_user(email: str,password: str,db):
    found_user = db.query(User).filter(User.email == email).first()
    if not found_user:
        return False
    if not bcrypt_context.verify(password,found_user.hashed_password): # verifie le mot de passe avec celui present dans la base donnee
        return False
    return found_user

# creation d'un token
def create_token(email: str,user_id: int,expire_delta: timedelta):
    encoded_data = {"sub":email,"id":user_id}

    expiration = datetime.now(timezone.utc) + expire_delta
    encoded_data.update({"expi": expiration.timestamp() })

    return jwt.encode(encoded_data, JWT_SECRET_KEY, JWT_ALGO)

async def get_current_player(token: Annotated[str, Depends(oauth2_bearer)]):

    try:
        payload = jwt.decode(
            token,  # Le jeton (chaîne) à décoder
            JWT_SECRET_KEY,  # La clé secrète utilisée pour la signature
            algorithms=JWT_ALGO  # L'algorithme de chiffrement
        )

        email: str = payload.get("sub")
        # 'id' est un champ personnalisé pour l'ID de l'utilisateur.
        user_id: int = payload.get("id")

        if email is None or user_id is None:
            # Si les informations nécessaires sont manquantes, lève une erreur 401.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="wrong credentials"  # Message générique de sécurité
            )
        return {"username": email, "id": user_id}

    except JWTError:
        # En cas d'échec de la vérification JWT, lève une erreur 401 (Unauthorized).
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="wrong credentials"  #un message d'erreur 
        )

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register_user(db: db_dependancy,user: UserValidation = Body()):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="User already registered")
    new_user = User(
        nom=user.nom,
        prenom=user.prenom,
        telephone=user.telephone,
        email=user.email,
        hashed_password=bcrypt_context.hash(user.password),
        enterprise_name=user.enterprise_name,
        enterprise_address=user.enterprise_address,
        employees_number=user.employees_number,
        aproximative_ca=user.aproximative_ca,
        secteur_activite=user.secteur_activite
    )
    db.add(new_user)
    db.commit()
    

# endpoint pour le login des user
@router.post("/login",response_model=Token,status_code=status.HTTP_200_OK)
async def login_player(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], db: db_dependancy):
    user_authenticated = authenticate_user(form_data.username,form_data.password,db)

    if not user_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="wrong credentials")

    token = create_token(user_authenticated.email,user_authenticated.id,timedelta(minutes=30))
    return {"access_token":token,"token_type": "Bearer"}
    