
from fastapi import APIRouter, Depends, HTTPException, Body, Path
from database import db_dependancy
from sqlalchemy import text
from starlette import status
from endpoints.simulateur_prix import SimulateurPrixRequest, simulation_complete
from endpoints.simulation_embauche import SimulateurEmbaucheRequest, calculer_cout_embauche_complet
from models import User
from comparative_ca import ComparativeCARequest, analyse_comparative_complete, comprative_ca_r
import joblib
import numpy as np
from pydantic import BaseModel, Field
from simulateur_lancement import SimulateurLancementRequest, simulateur

router = APIRouter(
    tags=["data_endpoint"],
    prefix="/data"
)

# Définir les modèles Pydantic dans le même fichier
class PaybackPeriodRequest(BaseModel):
    """Modèle de données pour la requête de calcul du délai de rentabilité"""
    
    Investissement_init: float = Field(
        ...,
        gt=0,
        description="Montant de l'investissement initial en euros",
        example=100000.0
    )
    
    Taux_de_marge_brut: float = Field(
        ...,
        ge=0,
        le=1,
        description="Taux de marge brute (entre 0 et 1, où 0.25 = 25%)",
        example=0.25
    )
    
    Taux_croissance_Ca: float = Field(
        ...,
        ge=0,
        le=1,
        description="Taux de croissance du chiffre d'affaires (entre 0 et 1)",
        example=0.1
    )
    
    BFR: float = Field(
        ...,
        ge=0,
        le=1,
        description="Besoin en fonds de roulement (entre 0 et 1)",
        example=0.15
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "Investissement_init": 100000.0,
                "Taux_de_marge_brut": 0.25,
                "Taux_croissance_Ca": 0.1,
                "BFR": 0.15
            }
        }

class PaybackPeriodResponse(BaseModel):
    """Modèle de réponse pour le délai de rentabilité"""
    
    delai_rentabilite: float = Field(
        ...,
        description="Délai de rentabilité estimé",
        example=24.5
    )
    
    unite: str = Field(
        default="mois",
        description="Unité de temps du délai de rentabilité"
    )
    
    parametres_utilises: dict = Field(
        ...,
        description="Paramètres utilisés pour le calcul"
    )
    
    message: str = Field(
        ...,
        description="Message descriptif du résultat"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "delai_rentabilite": 24.5,
                "unite": "mois",
                "parametres_utilises": {
                    "investissement_initial": 100000.0,
                    "taux_marge_brut": 0.25,
                    "taux_croissance_ca": 0.1,
                    "bfr": 0.15
                },
                "message": "Le délai de rentabilité estimé est de 24.50 mois"
            }
        }

# Charger le modèle une seule fois au démarrage
try:
    model = joblib.load("model_rentabilite.joblib")
except Exception as e:
    print(f"Erreur lors du chargement du modèle : {e}")
    model = None

@router.get("/hearbeat")
async def heartbeat(db: db_dependancy):
    """Vérifie la connexion à la base de données"""
    try:
        db.execute(text("SELECT 1"))
        return {"message": "DATABASE OK"}
    except Exception as e:
        return {"error": str(e)}

# Endpoint POST pour l'analyse comparative
@router.post("/comparative_ca", status_code=status.HTTP_200_OK)
async def comparative_ca_endpoint(donnees: ComparativeCARequest):
    """
    Analyse comparative du chiffre d'affaires entre deux périodes
    """
    try:
        # Préparation des données
        donnees_p1 = {
            "montants": donnees.montants_p1,
            "volumes": donnees.volumes_p1,
            "clients": donnees.clients_p1
        }
        
        donnees_p2 = {
            "montants": donnees.montants_p2,
            "volumes": donnees.volumes_p2,
            "clients": donnees.clients_p2
        }
        
        # Validation des données
        if not donnees_p1["montants"] or not donnees_p2["montants"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Les listes de montants pour les deux périodes sont requises"
            )
        
        # Exécution de l'analyse
        resultats = analyse_comparative_complete(donnees_p1, donnees_p2)
        
        return {
            "success": True,
            "data": resultats,
            "metadata": {
                "periodes_analysees": 2,
                "taux_remplissage": {
                    "montants": "100%",
                    "volumes": "100%" if donnees.volumes_p1 and donnees.volumes_p2 else "partiel",
                    "clients": "100%" if donnees.clients_p1 and donnees.clients_p2 else "partiel"
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'analyse comparative: {str(e)}"
        )

# Endpoint GET pour l'analyse par défaut (optionnel)
@router.get("/comparative_ca_default", status_code=status.HTTP_200_OK)
async def comparative_ca_default():
    """
    Analyse comparative avec des données par défaut (à des fins de démonstration)
    """
    # Données d'exemple
    donnees_exemple = ComparativeCARequest(
        montants_p1=[100.50, 200.75, 150.25, 300.00],
        montants_p2=[120.00, 250.50, 180.75, 350.00],
        volumes_p1=[1, 2, 1, 3],
        volumes_p2=[2, 3, 2, 4],
        clients_p1=["CL001", "CL002", "CL003"],
        clients_p2=["CL001", "CL002", "CL004", "CL005"]
    )
    
    donnees_p1 = {
        "montants": donnees_exemple.montants_p1,
        "volumes": donnees_exemple.volumes_p1,
        "clients": donnees_exemple.clients_p1
    }
    
    donnees_p2 = {
        "montants": donnees_exemple.montants_p2,
        "volumes": donnees_exemple.volumes_p2,
        "clients": donnees_exemple.clients_p2
    }
    
    resultats = analyse_comparative_complete(donnees_p1, donnees_p2)
    
    return {
        "success": True,
        "data": resultats,
        "note": "Ce sont des données d'exemple. Utilisez POST /data/comparative_ca avec vos propres données."
    }

@router.post("/simulateur_lancement_produit", status_code=status.HTTP_200_OK)
async def simulateur_lancement_produit(donnees: SimulateurLancementRequest):
    """
    Simule la rentabilité d'un nouveau produit
    """
    try:
        # Convertir le modèle Pydantic en dict
        donnees_dict = donnees.dict()
        
        # Exécuter la simulation
        resultat_simulation = simulateur.executer_simulation(donnees_dict)
        
        # Vérifier s'il y a des erreurs de validation
        if "erreur" in resultat_simulation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=resultat_simulation["erreur"]
            )
        
        return resultat_simulation
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la simulation: {str(e)}"
        )


@router.post("/simulateur_prix", status_code=status.HTTP_200_OK)
async def simulateur_prix_endpoint(donnees: SimulateurPrixRequest):
    """
    Simulateur de prix - Analyse l'impact d'un changement de prix sur le volume et le CA
    """
    try:
        # Validation des données
        if donnees.prix_actuel <= 0 or donnees.volume_actuel <= 0 or donnees.prix_nouveau <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tous les prix et volumes doivent être positifs"
            )
        
        if donnees.elasticite <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="L'élasticité doit être positive"
            )
        
        # Simulation complète
        resultat = simulation_complete(
            prix_actuel=donnees.prix_actuel,
            volume_actuel=donnees.volume_actuel,
            prix_nouveau=donnees.prix_nouveau,
            elasticite=donnees.elasticite
        )
        
        # Générer un résumé et des recommandations détaillées
        var_ca = resultat["chiffres_cles"]["variation_ca_pct"]
        var_volume = resultat["chiffres_cles"]["variation_volume_estime_pct"]
        var_prix = resultat["chiffres_cles"]["variation_prix_pct"]
        
        if var_ca > 0:
            recommandation = {
                "titre": "CHANGEMENT RECOMMANDÉ",
                "message": f"Le changement de prix augmenterait le CA de {var_ca:.1f}%.",
                "icone": "📈",
                "niveau": "success",
                "actions": [
                    f"Implémenter le nouveau prix de {resultat['chiffres_cles']['prix_nouveau']}",
                    "Communiquer la valeur ajoutée",
                    "Surveiller les réactions du marché"
                ]
            }
        elif var_ca < -10:
            recommandation = {
                "titre": "CHANGEMENT DÉCONSEILLÉ",
                "message": f"Le changement de prix réduirait le CA de {abs(var_ca):.1f}%.",
                "icone": "📉",
                "niveau": "danger",
                "actions": [
                    "Revoir la proposition de prix",
                    "Analyser la concurrence",
                    "Étudier des alternatives promotionnelles"
                ]
            }
        else:
            recommandation = {
                "titre": "IMPACT LIMITÉ",
                "message": f"Le changement de prix aurait un impact limité sur le CA ({var_ca:.1f}%).",
                "icone": "⚖️",
                "niveau": "warning",
                "actions": [
                    "Analyser les coûts additionnels",
                    "Évaluer l'impact sur l'image de marque",
                    "Considérer d'autres stratégies"
                ]
            }
        
        # Calculer des indicateurs complémentaires
        ca_actuel = resultat["chiffres_cles"]["ca_actuel"]
        ca_nouveau = resultat["chiffres_cles"]["ca_nouveau"]
        
        analyse_complementaire = {
            "impact_financier": {
                "delta_ca": round(ca_nouveau - ca_actuel, 2),
                "delta_ca_pct": var_ca,
                "point_mort_volume": round(resultat["chiffres_cles"]["volume_requis"], 2)
            },
            "elasticite_calculée": {
                "elasticite_prix": donnees.elasticite,
                "elasticite_effet": round(abs(var_volume / var_prix) if var_prix != 0 else 0, 2),
                "interpretation": "Élastique" if abs(var_volume / var_prix) > 1 else "Inélastique"
            }
        }
        
        # Retourner le résultat complet
        return {
            "success": True,
            "simulation": resultat,
            "recommandation": recommandation,
            "analyse_complementaire": analyse_complementaire,
            "summary": {
                "prix_actuel": donnees.prix_actuel,
                "prix_propose": donnees.prix_nouveau,
                "variation_prix": f"{var_prix:.1f}%",
                "variation_volume": f"{var_volume:.1f}%",
                "variation_ca": f"{var_ca:.1f}%",
                "decision": recommandation["titre"],
                "risque": recommandation["niveau"]
            }
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Données invalides : {str(e)}"
        )
    except ZeroDivisionError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Division par zéro - vérifiez les valeurs nulles"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la simulation : {str(e)}"
        )

# Endpoint GET pour l'exemple existant (compatibilité)
@router.get("/simulateur_prix_exemple", status_code=status.HTTP_200_OK)
async def simulateur_prix_exemple():
    """
    Exemple d'utilisation du simulateur de prix avec les données par défaut
    """
    donnees_simulation = {
        "prix_actuel": 5000,
        "volume_actuel": 100,
        "prix_nouveau": 4250,
        "elasticite": 1.2
    }
    
    resultat = simulation_complete(
        donnees_simulation["prix_actuel"],
        donnees_simulation["volume_actuel"],
        donnees_simulation["prix_nouveau"],
        donnees_simulation["elasticite"]
    )
    
    return {
        "success": True,
        "simulation": resultat,
        "note": "Données d'exemple : prix actuel 5000, volume 100, nouveau prix 4250"
    }

# Endpoint GET original (pour compatibilité)
@router.get("/simulateur_prix_legacy")
async def simulateur_prix_legacy():
    """Version legacy avec données fixes"""
    donnees_simulation = {
        "prix_actuel": 5000,
        "volume_actuel": 100,
        "prix_nouveau": 4250
    }
    
    resultat = simulation_complete(
        donnees_simulation["prix_actuel"],
        donnees_simulation["volume_actuel"],
        donnees_simulation["prix_nouveau"]
    )
    
    return resultat


@router.post("/simulateur_embauche", status_code=status.HTTP_200_OK)
async def simulateur_embauche_endpoint(donnees: SimulateurEmbaucheRequest):
    """
    Simulateur d'embauche - Calcule le coût total d'un employé et le CA nécessaire pour le rentabiliser
    """
    try:
        # Validation supplémentaire
        if donnees.salaire_brut <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le salaire brut doit être supérieur à 0"
            )
        
        if donnees.marge_entreprise <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La marge de l'entreprise doit être supérieure à 0%"
            )
        
        # Calcul complet
        resultat = calculer_cout_embauche_complet(
            salaire_brut=donnees.salaire_brut,
            taux_charges=donnees.taux_charges,
            frais_initiaux=donnees.frais_initiaux,
            marge_entreprise=donnees.marge_entreprise,
            marge_securite=donnees.marge_securite
        )
        
        # Ajouter des recommandations
        ca_min_mensuel = resultat["chiffre_affaires_requis"]["minimum_mensuel"]
        ratio_rentabilite = resultat["analyse_rentabilite"]["ratio_rentabilite"]
        
        if ratio_rentabilite < 1:
            recommandation = {
                "niveau": "danger",
                "titre": "EMPLOYÉ NON RENTABLE",
                "message": f"Le CA mensuel nécessaire ({ca_min_mensuel:.2f} €) est supérieur aux revenus que l'employé peut générer.",
                "actions": [
                    "Réévaluez le salaire proposé",
                    "Augmentez la productivité attendue",
                    "Considérez un contrat à temps partiel"
                ]
            }
        elif ratio_rentabilite < 1.3:
            recommandation = {
                "niveau": "warning",
                "titre": "RENTABILITÉ LIMITE",
                "message": f"La rentabilité est juste au seuil. Surveillez attentivement les performances.",
                "actions": [
                    "Définissez des objectifs de performance clairs",
                    "Prévoyez une période d'essai",
                    "Évaluez les compétences supplémentaires"
                ]
            }
        else:
            recommandation = {
                "niveau": "success",
                "titre": "EMPLOYÉ RENTABLE",
                "message": f"L'embauche est économiquement viable avec un CA mensuel cible de {ca_min_mensuel:.2f} €.",
                "actions": [
                    "Validez le recrutement",
                    "Planifiez l'intégration",
                    "Définissez des indicateurs de performance"
                ]
            }
        
        # Ajouter la recommandation au résultat
        resultat["recommandation"] = recommandation
        
        return {
            "success": True,
            "data": resultat,
            "summary": {
                "cout_total_premiere_annee": resultat["cout_premiere_annee"]["total"],
                "ca_mensuel_requis": resultat["chiffre_affaires_requis"]["minimum_mensuel"],
                "rentabilite": resultat["analyse_rentabilite"]["interpretation"]
            }
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Données invalides : {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du calcul : {str(e)}"
        )

# Endpoint GET pour démonstration (optionnel)
@router.get("/simulateur_embauche_exemple", status_code=status.HTTP_200_OK)
async def simulateur_embauche_exemple():
    """
    Exemple d'utilisation du simulateur d'embauche avec des données par défaut
    """
    donnees_exemple = SimulateurEmbaucheRequest(
        salaire_brut=3000.0,
        taux_charges=20.0,
        frais_initiaux=2000.0,
        marge_entreprise=25.0,
        marge_securite=30.0
    )
    
    resultat = calculer_cout_embauche_complet(
        salaire_brut=donnees_exemple.salaire_brut,
        taux_charges=donnees_exemple.taux_charges,
        frais_initiaux=donnees_exemple.frais_initiaux,
        marge_entreprise=donnees_exemple.marge_entreprise,
        marge_securite=donnees_exemple.marge_securite
    )
    
    return {
        "success": True,
        "data": resultat,
        "note": "Exemple avec salaire brut de 3000€, taux de charges 20%, frais initiaux 2000€, marge entreprise 25%"
    }

@router.post("/payback_period", status_code=status.HTTP_200_OK, response_model=PaybackPeriodResponse)
async def payback_period(caracteristiques: PaybackPeriodRequest):
    """
    Calcule le délai de rentabilité (payback period) basé sur les caractéristiques fournies
    """
    # Vérifier si le modèle est chargé
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Modèle non chargé. Veuillez contacter l'administrateur."
        )
    
    try:
        # Préparation des données pour la prédiction
        features = np.array([[
            caracteristiques.Investissement_init,
            caracteristiques.Taux_de_marge_brut,
            caracteristiques.Taux_croissance_Ca,
            caracteristiques.BFR
        ]])
        
        # Prédiction
        delai = model.predict(features)[0]
        
        # Formater le résultat
        delai_formate = float(delai)
        
        return PaybackPeriodResponse(
            delai_rentabilite=delai_formate,
            unite="mois",
            parametres_utilises={
                "investissement_initial": caracteristiques.Investissement_init,
                "taux_marge_brut": caracteristiques.Taux_de_marge_brut,
                "taux_croissance_ca": caracteristiques.Taux_croissance_Ca,
                "bfr": caracteristiques.BFR
            },
            message=f"Le délai de rentabilité estimé est de {delai_formate:.2f} mois"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Format de données invalide : {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du calcul du délai de rentabilité : {str(e)}"
        )