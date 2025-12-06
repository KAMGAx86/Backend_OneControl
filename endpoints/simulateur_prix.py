from typing import Annotated, Dict, Any
from pydantic import BaseModel, Field

 #Modèle Pydantic pour le simulateur de prix
class SimulateurPrixRequest(BaseModel):
    """Modèle pour le simulateur de prix"""
    prix_actuel: float = Field(
        ...,
        gt=0,
        description="Prix actuel du produit",
        example=5000.0
    )
    volume_actuel: float = Field(
        ...,
        gt=0,
        description="Volume de vente actuel",
        example=100.0
    )
    prix_nouveau: float = Field(
        ...,
        gt=0,
        description="Nouveau prix proposé",
        example=4250.0
    )
    elasticite: float = Field(
        default=1.2,
        gt=0,
        description="Élasticité prix de la demande",
        example=1.2
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "prix_actuel": 5000.0,
                "volume_actuel": 100.0,
                "prix_nouveau": 4250.0,
                "elasticite": 1.2
            }
        }

# Vos fonctions de calcul (gardez-les telles quelles)
def actuel_CA(prix_actuel, volume_actuel):
    """Calcule le chiffre d'affaires actuel"""
    return prix_actuel * volume_actuel

def variation_prix(prix_nouveau, prix_actuel):
    """Calcule la variation de prix en pourcentage"""
    if prix_actuel == 0:
        return 0
    return ((prix_nouveau - prix_actuel) / prix_actuel) * 100

def volume_requis(prix_actuel, volume_actuel, prix_nouveau):
    """Calcule le volume requis pour maintenir le même CA"""
    ca_actuel = actuel_CA(prix_actuel, volume_actuel)
    if prix_nouveau == 0:
        return float('inf'), float('inf')
    volume_requis = ca_actuel / prix_nouveau
    variation_volume_requis = volume_requis - volume_actuel
    return volume_requis, variation_volume_requis

def volume_estime(volume_actuel, variation_prix, elasticite=1.2):
    """Estime le nouveau volume basé sur l'élasticité prix"""
    variation_volume_pct = -elasticite * (variation_prix / 100)
    volume_estime = volume_actuel * (1 + variation_volume_pct)
    return volume_estime

def nouveau_CA(prix_nouveau, volume_estime):
    """Calcule le nouveau chiffre d'affaires"""
    return prix_nouveau * volume_estime

def variation_CA(ca_nouveau, ca_actuel):
    """Calcule la variation du CA en pourcentage"""
    if ca_actuel == 0:
        return 0
    return ((ca_nouveau - ca_actuel) / ca_actuel) * 100

def simulation_complete(prix_actuel, volume_actuel, prix_nouveau, elasticite=1.2):
    """Fonction complète de simulation de prix"""
    # CA actuel
    ca_actuel = actuel_CA(prix_actuel, volume_actuel)
    
    # Variation de prix
    var_prix = variation_prix(prix_nouveau, prix_actuel)
    
    # Volume requis pour maintenir le CA
    vol_requis, var_vol_requis = volume_requis(prix_actuel, volume_actuel, prix_nouveau)
    
    # Volume estimé basé sur l'élasticité
    vol_estime = volume_estime(volume_actuel, var_prix, elasticite)
    
    # Nouveau CA estimé
    ca_nouveau = nouveau_CA(prix_nouveau, vol_estime)
    
    # Variation du CA
    var_ca = variation_CA(ca_nouveau, ca_actuel)
    
    # Variation du volume estimé en %
    if volume_actuel != 0:
        var_vol_estime_pct = ((vol_estime - volume_actuel) / volume_actuel) * 100
    else:
        var_vol_estime_pct = 0
    
    # Marge sur coût variable (exemple)
    cout_variable = prix_actuel * 0.6  # 60% de coût variable
    marge_actuelle = (prix_actuel - cout_variable) * volume_actuel
    marge_nouvelle = (prix_nouveau - cout_variable) * vol_estime if prix_nouveau > cout_variable else 0
    
    # Analyse de rentabilité
    seuil_rentabilite = cout_variable * volume_actuel
    rentabilite_actuelle = ca_actuel > seuil_rentabilite
    rentabilite_nouvelle = ca_nouveau > seuil_rentabilite
    
    # Analyse de sensibilité
    scenarios = []
    variations = [-10, -5, 0, 5, 10]  # Variations de prix en %
    for var in variations:
        prix_scenario = prix_nouveau * (1 + var/100)
        vol_scenario = volume_estime(volume_actuel, variation_prix(prix_scenario, prix_actuel), elasticite)
        ca_scenario = nouveau_CA(prix_scenario, vol_scenario)
        scenarios.append({
            "variation_prix_pct": var,
            "prix_scenario": round(prix_scenario, 2),
            "volume_scenario": round(vol_scenario, 2),
            "ca_scenario": round(ca_scenario, 2),
            "rentable": ca_scenario > (cout_variable * vol_scenario)
        })
    
    return {
        "donnees_entree": {
            "prix_actuel": round(prix_actuel, 2),
            "volume_actuel": round(volume_actuel, 2),
            "prix_nouveau": round(prix_nouveau, 2),
            "elasticite": elasticite
        },
        "chiffres_cles": {
            "prix_nouveau": round(prix_nouveau, 2),
            "variation_prix_pct": round(var_prix, 2),
            "ca_actuel": round(ca_actuel, 2),
            "volume_requis": round(vol_requis, 2),
            "variation_volume_requis": round(var_vol_requis, 2),
            "volume_estime": round(vol_estime, 2),
            "variation_volume_estime_pct": round(var_vol_estime_pct, 2),
            "ca_nouveau": round(ca_nouveau, 2),
            "variation_ca_pct": round(var_ca, 2)
        },
        "analyse_rentabilite": {
            "cout_variable_unitaire": round(cout_variable, 2),
            "marge_actuelle": round(marge_actuelle, 2),
            "marge_nouvelle": round(marge_nouvelle, 2),
            "variation_marge_pct": round(((marge_nouvelle - marge_actuelle) / marge_actuelle * 100) if marge_actuelle != 0 else 0, 2),
            "seuil_rentabilite": round(seuil_rentabilite, 2),
            "rentabilite_actuelle": rentabilite_actuelle,
            "rentabilite_nouvelle": rentabilite_nouvelle
        },
        "analyse_sensibilite": scenarios,
        "recommandation": {
            "decision": "Augmentation" if var_ca > 0 else "Maintenir" if var_ca == 0 else "Revoir",
            "niveau_risque": "Faible" if abs(var_ca) < 5 else "Modéré" if abs(var_ca) < 15 else "Élevé",
            "optimisation": "Prix optimal" if var_ca > 0 and rentabilite_nouvelle else "Ajustement nécessaire"
        }
    }