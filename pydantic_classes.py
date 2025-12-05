from typing import Optional
from pydantic import BaseModel,Field, constr


class UserValidation(BaseModel):
    
    nom : str = Field(description="Nom de l'utilisateur",min_length=2)
    prenom : str = Field(description="Prenom de l'utilisateur",min_length=2)
    telephone : str = Field(description="Telephone de l'utilisateur",min_length=8,max_length=15)
    email : str = Field(description="Email de l'utilisateur")
    password : str = Field(description="mot de passe de l'utilisateur",min_length=8)
    enterprise_name : str = Field(description="Nom de l'entreprise",min_length=2)
    enterprise_address : str = Field(description="Adresse de l'entreprise",min_length=2)
    employees_number : int = Field(description="Nombre d'employes dans l'entreprise",ge=1)
    aproximative_ca : str = Field(description="Chiffre d'affaire aproximatif de l'entreprise",min_length=1)
    secteur_activite : str = Field(description="Secteur d'activite de l'entreprise",min_length=2)
        
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "nom": "Doe",
                "prenom": "John",
                "telephone": "12345678",
                "email": "jesuis@gmail.com",
                "password": "12345678",
                "enterprise_name": "Tech Solutions",
                "enterprise_address": "123 Tech Street, Silicon Valley",
                "employees_number": 50,
                "aproximative_ca": "5M-10M",
                "secteur_activite": "Information Technology",
            } 
        }
    }
    

class UserLoginValidation(BaseModel):
    email : str = Field(description="Email de l'utilisateur")
    password : str = Field(description="mot de passe de l'utilisateur",min_length=8)


# classe qui represente un modele de retour de toknen de connexion
class Token(BaseModel):
    access_token: str
    token_type: str
    

class SimpleResetRequest(BaseModel):
    token: Optional[str] = None
    new_password: Optional[str] = None