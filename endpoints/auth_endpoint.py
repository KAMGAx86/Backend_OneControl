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
from emails import envoyer_email

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

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):

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


# HELPER FUNCTION FOR PASSWORD RESET

def generate_simple_token():
    """Genere un token simple avec le module secrets de python"""
    import secrets
    return ''.join(secrets.choice('0123456789') for _ in range(12))

def is_token_valid(token_expiry):
    """
    Verifie si le token est encore valide en comparant la date d'expiration avec la date actuelle
    """
    from datetime import datetime, timezone
    if not token_expiry:
        return False
    return datetime.now(timezone.utc) < token_expiry


####################

@router.post("/forgot-password")
async def forgot_password(db: db_dependancy,email : str = Body()):
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Aucun utilisateur avec cet email"
        )
        
    token = generate_simple_token()
    
    #defiinir l'expiration 15 minutes
    from datetime import datetime, timezone, timedelta
    expiry = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # sauvegarder dans la table user
    user.reset_token = token
    user.token_expiry = expiry
    db.commit()
    
    #envoie l'email
    envoyer_email(email,"Réinitialisation de mot de passe",f"Votre code de réinitialisation est : {token}")
    
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Un code de réinitialisation a été envoyé"
    )
    
@router.post("/reset-password")
async def reset_password(db: db_dependancy,token: str = Body(), new_password: str = Body(), ):
    """
    Réinitialisation avec token
    - L'utilisateur donne le token reçu
    - Et son nouveau mot de passe
    """
    
    #Chercher l'utilisateur avec ce token
    user = db.query(User).filter(
        User.reset_token == token
    ).first()
    
    #Vérifier s'il existe et si le token est valide
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    
    if not is_token_valid(user.token_expiry):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="token expired"
        )
    
    #Mettre à jour le mot de passe
    user.hashed_password = bcrypt_context.hash(new_password)
    
    #Invalider le token
    user.reset_token = None
    user.token_expiry = None
    
    db.commit()
    
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="password changed successfully"
    )
    