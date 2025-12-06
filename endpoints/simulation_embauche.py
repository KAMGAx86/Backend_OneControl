from pydantic import BaseModel, Field

# Modèle Pydantic pour le simulateur d'embauche
class SimulateurEmbaucheRequest(BaseModel):
    """Modèle pour le simulateur d'embauche"""
    salaire_brut: float = Field(
        ...,
        gt=0,
        description="Salaire brut mensuel de l'employé",
        example=3000.0
    )
    taux_charges: float = Field(
        default=20.0,
        ge=0,
        le=100,
        description="Taux de charges sociales patronales en %",
        example=20.0
    )
    frais_initiaux: float = Field(
        default=0.0,
        ge=0,
        description="Frais initiaux (formation, équipement, etc.)",
        example=2000.0
    )
    marge_entreprise: float = Field(
        default=25.0,
        gt=0,
        le=100,
        description="Marge bénéficiaire de l'entreprise en %",
        example=25.0
    )
    marge_securite: float = Field(
        default=30.0,
        ge=0,
        description="Marge de sécurité en %",
        example=30.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "salaire_brut": 3000.0,
                "taux_charges": 20.0,
                "frais_initiaux": 2000.0,
                "marge_entreprise": 25.0,
                "marge_securite": 30.0
            }
        }

# Vos fonctions de calcul (gardez-les telles quelles)
def charge_social_patronal_mensuel(employee_salaire, taux_de_charge_social=20.0):
    """
    Calcule les charges sociales patronales mensuelles.
    """
    taux_decimal = taux_de_charge_social / 100
    charges = employee_salaire * taux_decimal
    return {"charge_social_patronal": charges}

def cout_mensuel_total(employee_salaire, charge_social_patronal):
    """
    Calcule le coût mensuel total pour l'employeur.
    """
    cout_total = employee_salaire + charge_social_patronal
    return {"cout_mensuel_total": cout_total}

def cout_annuel(cout_mensuel_total):
    """
    Calcule le coût annuel de l'employé.
    """
    cout_annuel = cout_mensuel_total * 12
    return {"cout_annuel": cout_annuel}

def cout_premiere_annee(cout_annuel, frais_supplementaire=0):
    """
    Calcule le coût total de la première année incluant les frais initiaux.
    """
    cout_total = cout_annuel + frais_supplementaire
    return {"cout_premiere_annee": cout_total}

def marge_beneficiaire(benefices, CA):
    """
    Calcule la marge bénéficiaire de l'entreprise en pourcentage.
    """
    if CA == 0:
        return {"marge_beneficiaire": 0.0, "error": "CA ne peut pas être zéro"}
    
    marge = (benefices / CA) * 100
    return {"marge_beneficiaire": marge}

def ca_minimum(cout_mensuel, marge_beneficiaire_pourcent):
    """
    Calcule le chiffre d'affaires minimum requis pour rentabiliser l'employé.
    """
    if marge_beneficiaire_pourcent == 0:
        return {"ca_minimum": float('inf'), "error": "Marge ne peut pas être 0%"}
    
    marge_decimal = marge_beneficiaire_pourcent / 100
    ca_min = cout_mensuel / marge_decimal
    return {"ca_minimum": ca_min}

def ca_securise(ca_minimum, marge_securite_pourcent=30):
    """
    Calcule le chiffre d'affaires sécurisé avec une marge de sécurité.
    """
    multiplicateur_securite = 1 + (marge_securite_pourcent / 100)
    ca_sec = ca_minimum * multiplicateur_securite
    return {"ca_securise": ca_sec}

def calculer_cout_embauche_complet(
    salaire_brut, 
    taux_charges=20.0, 
    frais_initiaux=0, 
    marge_entreprise=25.0,
    marge_securite=30.0
):
    """
    Fonction complète pour calculer tous les coûts d'embauche.
    """
    # 1. Calcul des charges sociales
    charges = charge_social_patronal_mensuel(salaire_brut, taux_charges)
    montant_charges = charges["charge_social_patronal"]
    
    # 2. Calcul du coût mensuel total
    cout_mensuel = cout_mensuel_total(salaire_brut, montant_charges)
    montant_cout_mensuel = cout_mensuel["cout_mensuel_total"]
    
    # 3. Calcul du coût annuel
    cout_annuel_result = cout_annuel(montant_cout_mensuel)
    montant_cout_annuel = cout_annuel_result["cout_annuel"]
    
    # 4. Calcul du coût première année
    cout_premiere = cout_premiere_annee(montant_cout_annuel, frais_initiaux)
    montant_cout_premiere = cout_premiere["cout_premiere_annee"]
    
    # 5. Calcul du CA minimum
    ca_min = ca_minimum(montant_cout_mensuel, marge_entreprise)
    montant_ca_min = ca_min["ca_minimum"]
    
    # 6. Calcul du CA sécurisé
    ca_sec = ca_securise(montant_ca_min, marge_securite)
    montant_ca_sec = ca_sec["ca_securise"]
    
    # 7. Analyse de la rentabilité
    rentabilite_mois = montant_ca_min / montant_cout_mensuel
    rentabilite_mois_securise = montant_ca_sec / montant_cout_mensuel
    
    # Retour de tous les résultats
    return {
        "salaire_brut": salaire_brut,
        "charges_sociales": {
            "montant": round(montant_charges, 2),
            "taux": taux_charges,
            "part_salaire": round((montant_charges / salaire_brut) * 100, 2) if salaire_brut > 0 else 0
        },
        "cout_mensuel": {
            "total": round(montant_cout_mensuel, 2),
            "dont_salaire": round(salaire_brut, 2),
            "dont_charges": round(montant_charges, 2)
        },
        "cout_annuel": {
            "total": round(montant_cout_annuel, 2),
            "moyen_mensuel": round(montant_cout_annuel / 12, 2)
        },
        "cout_premiere_annee": {
            "total": round(montant_cout_premiere, 2),
            "dont_frais_initiaux": round(frais_initiaux, 2)
        },
        "chiffre_affaires_requis": {
            "minimum_mensuel": round(montant_ca_min, 2),
            "securise_mensuel": round(montant_ca_sec, 2),
            "minimum_annuel": round(montant_ca_min * 12, 2),
            "securise_annuel": round(montant_ca_sec * 12, 2)
        },
        "analyse_rentabilite": {
            "ratio_rentabilite": round(rentabilite_mois, 2),
            "ratio_securise": round(rentabilite_mois_securise, 2),
            "interpretation": "Rentable" if rentabilite_mois > 1 else "Non rentable",
            "niveau_securite": "Bon" if rentabilite_mois_securise > 1.5 else "Moyen" if rentabilite_mois_securise > 1 else "Faible"
        },
        "parametres_utilises": {
            "marge_entreprise": marge_entreprise,
            "marge_securite": marge_securite
        }
    }