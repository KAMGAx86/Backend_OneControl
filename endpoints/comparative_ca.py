from pydantic import BaseModel, Field
from typing import List

# Modèles Pydantic pour les requêtes
class ComparativeCARequest(BaseModel):
    """Modèle pour les données d'analyse comparative"""
    montants_p1: List[float] = Field(
        ...,
        description="Liste des montants des transactions pour la période 1",
        example=[100.50, 200.75, 150.25]
    )
    montants_p2: List[float] = Field(
        ...,
        description="Liste des montants des transactions pour la période 2",
        example=[120.00, 250.50, 180.75]
    )
    volumes_p1: List[float] = Field(
        default=[],
        description="Liste des volumes de marchandise pour la période 1",
        example=[1, 2, 3]
    )
    volumes_p2: List[float] = Field(
        default=[],
        description="Liste des volumes de marchandise pour la période 2",
        example=[2, 3, 4]
    )
    clients_p1: List[str] = Field(
        default=[],
        description="Liste des IDs clients pour la période 1",
        example=["CL001", "CL002", "CL003"]
    )
    clients_p2: List[str] = Field(
        default=[],
        description="Liste des IDs clients pour la période 2",
        example=["CL001", "CL002", "CL004"]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "montants_p1": [100.50, 200.75, 150.25],
                "montants_p2": [120.00, 250.50, 180.75],
                "volumes_p1": [1, 2, 3],
                "volumes_p2": [2, 3, 4],
                "clients_p1": ["CL001", "CL002", "CL003"],
                "clients_p2": ["CL001", "CL002", "CL004"]
            }
        }

# Copiez ici toutes vos fonctions de calcul (CA, volume, prix moyen, etc.)

def CA(liste_montant_transaction):
    """Calcule le CA total à partir d'une liste de montants"""
    if not liste_montant_transaction:
        return 0
    return sum(liste_montant_transaction)

def ComparativeCA_Kpi(liste_montant_transaction_p1, liste_montant_transaction_p2):
    """Compare le CA entre deux périodes avec gestion des cas limites"""
    CA_p1 = CA(liste_montant_transaction_p1)
    CA_p2 = CA(liste_montant_transaction_p2)
    
    if CA_p1 == 0:
        variation_ca = float('inf') if CA_p2 > 0 else 0
    else:
        variation_ca = round((CA_p2 - CA_p1) / CA_p1 * 100, 2)
    
    variation_absolue = CA_p2 - CA_p1
    
    return {
        "CA_p1": CA_p1,
        "CA_p2": CA_p2,
        "variation_absolue": variation_absolue,
        "variation_pourcentage": variation_ca
    }

def Volume(liste_volume_marchandise):
    """Calcule le volume total"""
    if not liste_volume_marchandise:
        return 0
    return sum(liste_volume_marchandise)

def Comparative_Volume_Kpi(liste_volume_marchandise_p1, liste_volume_marchandise_p2):
    """Compare le volume entre deux périodes"""
    Volume_p1 = Volume(liste_volume_marchandise_p1)
    Volume_p2 = Volume(liste_volume_marchandise_p2)
    
    if Volume_p1 == 0:
        variation_volume = float('inf') if Volume_p2 > 0 else 0
    else:
        variation_volume = round((Volume_p2 - Volume_p1) / Volume_p1 * 100, 2)
    
    return {
        "volume_p1": Volume_p1,
        "volume_p2": Volume_p2,
        "variation_pourcentage": variation_volume
    }

def prix_moyen(CA, volume_marchandise):
    """Calcule le prix moyen pondéré"""
    if volume_marchandise == 0:
        return 0
    return CA / volume_marchandise

def Comparative_prix_moyen(CA_p1, volume_marchandise_p1, CA_p2, volume_marchandise_p2):
    """Compare le prix moyen entre deux périodes"""
    prix_moyen_p1 = prix_moyen(CA_p1, volume_marchandise_p1)
    prix_moyen_p2 = prix_moyen(CA_p2, volume_marchandise_p2)
    
    if prix_moyen_p1 == 0:
        variation_prix_moyen = float('inf') if prix_moyen_p2 > 0 else 0
    else:
        variation_prix_moyen = round((prix_moyen_p2 - prix_moyen_p1) / prix_moyen_p1 * 100, 2)
    
    return {
        "prix_moyen_p1": prix_moyen_p1,
        "prix_moyen_p2": prix_moyen_p2,
        "variation_pourcentage": variation_prix_moyen
    }

def client_actif(liste_client_actif_p1, liste_client_actif_p2):
    """Identifie les clients actifs par période"""
    if not liste_client_actif_p1 or not liste_client_actif_p2:
        return {
            "clients_actifs_p1": 0,
            "clients_actifs_p2": 0,
            "variation_pourcentage": 0,
            "nouveaux_clients": 0,
            "clients_fideles": 0,
            "clients_perdus": 0,
            "taux_retention": 0
        }
    
    ensemble_client_unique_p1 = set(liste_client_actif_p1)
    ensemble_client_unique_p2 = set(liste_client_actif_p2)
    
    client_actif_p1 = len(ensemble_client_unique_p1)
    client_actif_p2 = len(ensemble_client_unique_p2)
    
    if client_actif_p1 == 0:
        variation_client_actif = float('inf') if client_actif_p2 > 0 else 0
    else:
        variation_client_actif = round((client_actif_p2 - client_actif_p1) / client_actif_p1 * 100, 2)
    
    # Identification des segments clients
    nouveaux_clients = ensemble_client_unique_p2 - ensemble_client_unique_p1
    clients_fideles = ensemble_client_unique_p1 & ensemble_client_unique_p2
    clients_perdus = ensemble_client_unique_p1 - ensemble_client_unique_p2
    
    return {
        "clients_actifs_p1": client_actif_p1,
        "clients_actifs_p2": client_actif_p2,
        "variation_pourcentage": variation_client_actif,
        "nouveaux_clients": len(nouveaux_clients),
        "clients_fideles": len(clients_fideles),
        "clients_perdus": len(clients_perdus),
        "taux_retention": round(len(clients_fideles) / client_actif_p1 * 100, 2) if client_actif_p1 > 0 else 0
    }

def decomposition_volume_prix(Q_total_produit_p1, Q_total_produit_p2, CA_total_p1, CA_total_p2):
    """Analyse complète de la décomposition volume/prix"""
    delta_ca = CA_total_p2 - CA_total_p1
    
    # Calcul des effets
    if Q_total_produit_p1 == 0:
        prix_moyen_pondere_p1 = 0
    else:
        prix_moyen_pondere_p1 = CA_total_p1 / Q_total_produit_p1
    
    volume_effet = (Q_total_produit_p2 - Q_total_produit_p1) * prix_moyen_pondere_p1
    
    if Q_total_produit_p2 == 0:
        prix_moyen_pondere_p2 = 0
    else:
        prix_moyen_pondere_p2 = CA_total_p2 / Q_total_produit_p2
    
    prix_effet = Q_total_produit_p1 * (prix_moyen_pondere_p2 - prix_moyen_pondere_p1)
    mix_effet = delta_ca - (volume_effet + prix_effet)
    
    # Pourcentages
    if delta_ca != 0:
        volume_percent = round((volume_effet / delta_ca) * 100, 2)
        prix_percent = round((prix_effet / delta_ca) * 100, 2)
        mix_percent = round((mix_effet / delta_ca) * 100, 2)
    else:
        volume_percent = prix_percent = mix_percent = 0
    
    # Vérification
    somme_effets = volume_effet + prix_effet + mix_effet
    erreur = abs(delta_ca - somme_effets)
    
    return {
        "delta_CA": round(delta_ca, 2),
        "effet_volume": {
            "valeur": round(volume_effet, 2),
            "pourcentage": volume_percent,
            "description": "Impact des changements de quantité"
        },
        "effet_prix": {
            "valeur": round(prix_effet, 2),
            "pourcentage": prix_percent,
            "description": "Impact des changements de prix"
        },
        "effet_mix": {
            "valeur": round(mix_effet, 2),
            "pourcentage": mix_percent,
            "description": "Impact du changement de composition"
        },
        "verification": {
            "somme_effets": round(somme_effets, 2),
            "erreur": round(erreur, 2),
            "est_correct": erreur < 0.01
        }
    }

# Fonction principale pour analyser les données
def analyse_comparative_complete(donnees_p1, donnees_p2):
    """
    Fonction principale pour une analyse complète
    """
    resultats = {}
    
    # Analyse CA
    resultats["ca"] = ComparativeCA_Kpi(donnees_p1["montants"], donnees_p2["montants"])
    
    # Analyse Volume
    volumes_p1 = donnees_p1.get("volumes", [])
    volumes_p2 = donnees_p2.get("volumes", [])
    resultats["volume"] = Comparative_Volume_Kpi(volumes_p1, volumes_p2)
    
    # Analyse Prix moyen
    if volumes_p1 and volumes_p2:
        resultats["prix_moyen"] = Comparative_prix_moyen(
            resultats["ca"]["CA_p1"], resultats["volume"]["volume_p1"],
            resultats["ca"]["CA_p2"], resultats["volume"]["volume_p2"]
        )
    else:
        resultats["prix_moyen"] = {
            "prix_moyen_p1": 0,
            "prix_moyen_p2": 0,
            "variation_pourcentage": 0
        }
    
    # Analyse Clients
    clients_p1 = donnees_p1.get("clients", [])
    clients_p2 = donnees_p2.get("clients", [])
    resultats["clients"] = client_actif(clients_p1, clients_p2)
    
    # Décomposition volume/prix
    if volumes_p1 and volumes_p2:
        resultats["decomposition"] = decomposition_volume_prix(
            resultats["volume"]["volume_p1"], resultats["volume"]["volume_p2"],
            resultats["ca"]["CA_p1"], resultats["ca"]["CA_p2"]
        )
    else:
        resultats["decomposition"] = {
            "delta_CA": resultats["ca"]["variation_absolue"],
            "effet_volume": {"valeur": 0, "pourcentage": 0, "description": "Données manquantes"},
            "effet_prix": {"valeur": 0, "pourcentage": 0, "description": "Données manquantes"},
            "effet_mix": {"valeur": 0, "pourcentage": 0, "description": "Données manquantes"}
        }
    
    # Résumé
    resultats["resume"] = {
        "periodes_comparables": len(donnees_p1["montants"]) > 0 and len(donnees_p2["montants"]) > 0,
        "nombres_transactions": {
            "p1": len(donnees_p1["montants"]),
            "p2": len(donnees_p2["montants"])
        },
        "performance_globale": "positive" if resultats["ca"]["variation_absolue"] > 0 else "negative" if resultats["ca"]["variation_absolue"] < 0 else "stable"
    }
    
    return resultats