


        

def calculer_marge(prix_vente, cout_production):

    marge_unitaire = prix_vente - cout_production
    pourcentage_marge = (marge_unitaire / prix_vente) * 100 if prix_vente > 0 else 0
    return {
        "unitaire": marge_unitaire, 
        "pourcentage": pourcentage_marge
    }

def calculer_seuil_rentabilite(couts_fixes, marge_unitaire):
    """Calcule le nombre d'unités nécessaires pour atteindre le seuil de rentabilité"""
    if marge_unitaire <= 0:
        return float('inf')
    seuil_unites = couts_fixes / marge_unitaire
    return seuil_unites

def calculer_delai_rentabilite(seuil_unites, volume_mensuel):
    """Calcule le délai en mois pour atteindre la rentabilité"""
    if volume_mensuel <= 0:
        return float('inf')
    delai_mois = seuil_unites / volume_mensuel
    return delai_mois

def calculer_roi(marge_unitaire, volume_mensuel, couts_fixes, periode=6):
    """Calcule le ROI et le profit net sur une période donnée"""
    profit_brut = marge_unitaire * volume_mensuel * periode
    profit_net = profit_brut - couts_fixes
    roi_pourcentage = (profit_net / couts_fixes) * 100 if couts_fixes > 0 else 0
    return roi_pourcentage, profit_net


# ============================================
# FONCTIONS D'ÉVALUATION DES RISQUES
# ============================================

def evaluer_risque_marge(pourcentage_marge):
    
    if pourcentage_marge > 50:
        return {
            "niveau": "faible",
            "niveau_en": "low",
            "score": min(pourcentage_marge, 100)
        }
    elif pourcentage_marge >= 20:
        return {
            "niveau": "moyen",
            "niveau_en": "medium",
            "score": pourcentage_marge
        }
    else:
        return {
            "niveau": "élevé",
            "niveau_en": "high",
            "score": pourcentage_marge
        }

def evaluer_risque_volume(volume_prevu, seuil_unites):
    
    if seuil_unites <= 0:
        return "indéterminé"
    
    ratio = volume_prevu / seuil_unites
    if ratio > 2:
        return "très faible"
    elif ratio > 1:
        return "faible"
    elif ratio > 0.5:
        return "moyen"
    else:
        return "élevé"

def generer_recommandation(roi, pourcentage_marge, delai_mois):
    
    if roi > 150 and pourcentage_marge > 40:
        return {
            "titre": "EXCELLENT PROJET",
            "message": "🚀 LANCER IMMÉDIATEMENT !",
            "icone": "🚀",
            "niveau": "success"
        }
    elif roi > 50 and pourcentage_marge > 20:
        return {
            "titre": "BON PROJET",
            "message": "✅ LANCER LE PROJET.",
            "icone": "✅",
            "niveau": "positive"
        }
    elif roi > 0:
        return {
            "titre": "PROJET VIABLE",
            "message": "⚠️ PRUDENCE RECOMMANDÉE.",
            "icone": "⚠️",
            "niveau": "warning"
        }
    else:
        return {
            "titre": "PROJET NON RENTABLE",
            "message": "❌ NE PAS LANCER.",
            "icone": "❌",
            "niveau": "danger"
        }



def calculer_projections(prix_vente, cout_production, volume_mensuel, couts_fixes, periode=6):
    
    periode_amortissement = 2
    

    ca_mois_1_2 = prix_vente * volume_mensuel * periode_amortissement
    couts_variables_1_2 = cout_production * volume_mensuel * periode_amortissement
    couts_mois_1_2 = couts_variables_1_2 + couts_fixes
    profit_mois_1_2 = ca_mois_1_2 - couts_mois_1_2

    periode_restante = periode - periode_amortissement
    ca_mois_3_6 = prix_vente * volume_mensuel * periode_restante
    couts_mois_3_6 = cout_production * volume_mensuel * periode_restante
    profit_mois_3_6 = ca_mois_3_6 - couts_mois_3_6
    
    ca_total = ca_mois_1_2 + ca_mois_3_6
    couts_total = couts_mois_1_2 + couts_mois_3_6
    profit_total = profit_mois_1_2 + profit_mois_3_6
    
    return {
        "mois_1_2": {
            "ca": ca_mois_1_2,
            "couts": couts_mois_1_2,
            "profit": profit_mois_1_2
        },
        "mois_3_6": {
            "ca": ca_mois_3_6,
            "couts": couts_mois_3_6,
            "profit": profit_mois_3_6
        },
        "total": {
            "ca": ca_total,
            "couts": couts_total,
            "profit": profit_total
        }
    }



class ValidateurDonnees:
    """Valide les données d'entrée"""
    
    def valider_donnees_entree(self, donnees):
        """Valide que toutes les données nécessaires sont présentes et valides"""
        erreurs = []
        
        champs_requis = ["prix_vente", "coût_production", "coûts_fixes", "volume_mensuel"]
        for champ in champs_requis:
            if champ not in donnees:
                erreurs.append(f"Le champ '{champ}' est manquant")
            elif not isinstance(donnees[champ], (int, float)):
                erreurs.append(f"Le champ '{champ}' doit être un nombre")
            elif donnees[champ] < 0:
                erreurs.append(f"Le champ '{champ}' ne peut pas être négatif")
        
        if "prix_vente" in donnees and "coût_production" in donnees:
            if donnees["prix_vente"] <= donnees["coût_production"]:
                erreurs.append("Le prix de vente doit être supérieur au coût de production")
        
        return {
            "valide": len(erreurs) == 0,
            "erreurs": erreurs
        }
    
    def calculer_indicateurs_alerte(self, donnees):

        alertes = []
        
        marge = calculer_marge(donnees["prix_vente"], donnees["coût_production"])
        if marge["pourcentage"] < 15:
            alertes.append("⚠️ Marge très faible (< 15%)")
        
        seuil = calculer_seuil_rentabilite(donnees["coûts_fixes"], marge["unitaire"])
        volume_prevu_6mois = donnees["volume_mensuel"] * 6
        if seuil > volume_prevu_6mois:
            alertes.append("⚠️ Seuil de rentabilité non atteint en 6 mois")
        
        if donnees["coûts_fixes"] > donnees["prix_vente"] * donnees["volume_mensuel"] * 3:
            alertes.append("⚠️ Coûts fixes très élevés par rapport au CA mensuel")
        
        return alertes


class CalculateurFinancier:
    
    def calculer_marge(self, prix_vente, cout_production):
        return calculer_marge(prix_vente, cout_production)
    
    def calculer_seuil_rentabilite(self, couts_fixes, marge_unitaire):
        return calculer_seuil_rentabilite(couts_fixes, marge_unitaire)
    
    def calculer_delai_rentabilite(self, seuil_unites, volume_mensuel):
        return calculer_delai_rentabilite(seuil_unites, volume_mensuel)
    
    def calculer_roi(self, marge_unitaire, volume_mensuel, couts_fixes, periode=6):
        return calculer_roi(marge_unitaire, volume_mensuel, couts_fixes, periode)


class AnalyseurRisque:
    
    
    def evaluer_risque_marge(self, pourcentage_marge):
        return evaluer_risque_marge(pourcentage_marge)
    
    def evaluer_risque_volume(self, volume_prevu, seuil_unites):
        return evaluer_risque_volume(volume_prevu, seuil_unites)
    
    def generer_recommandation(self, roi, pourcentage_marge, delai_mois):
        return generer_recommandation(roi, pourcentage_marge, delai_mois)


class ProjecteurFinancier:
    
    def generer_projection_mensuelle(self, donnees):
        return calculer_projections(
            donnees["prix_vente"],
            donnees["coût_production"],
            donnees["volume_mensuel"],
            donnees["coûts_fixes"]
        )


class SimulateurLancement:

    
    def __init__(self):
        self.calculateur = CalculateurFinancier()
        self.analyseur = AnalyseurRisque()
        self.projecteur = ProjecteurFinancier()
        self.validateur = ValidateurDonnees()
    
    def executer_simulation(self, donnees):

        validation = self.validateur.valider_donnees_entree(donnees)
        if not validation["valide"]:
            return {"erreur": validation["erreurs"]}
        
        marge = self.calculateur.calculer_marge(
            donnees["prix_vente"], 
            donnees["coût_production"]
        )
        
        seuil_unites = self.calculateur.calculer_seuil_rentabilite(
            donnees["coûts_fixes"], 
            marge["unitaire"]
        )
        
        delai_mois = self.calculateur.calculer_delai_rentabilite(
            seuil_unites, 
            donnees["volume_mensuel"]
        )
        
        roi, profit_6mois = self.calculateur.calculer_roi(
            marge["unitaire"],
            donnees["volume_mensuel"],
            donnees["coûts_fixes"]
        )
        
        risque = self.analyseur.evaluer_risque_marge(marge["pourcentage"])
        risque_volume = self.analyseur.evaluer_risque_volume(
            donnees["volume_mensuel"] * 6,
            seuil_unites
        )
        
        projections = self.projecteur.generer_projection_mensuelle(donnees)
        
        recommandation = self.analyseur.generer_recommandation(
            roi, marge["pourcentage"], delai_mois
        )

        return {
            "marge": marge,
            "seuil_rentabilite": {
                "unites": round(seuil_unites, 2),
                "delai_mois": round(delai_mois, 2)
            },
            "roi": {
                "pourcentage": round(roi, 2),
                "profit_6mois": round(profit_6mois, 2)
            },
            "risque": {
                "marge": risque,
                "volume": risque_volume
            },
            "projections": projections,
            "recommandation": recommandation,
            "alertes": self.validateur.calculer_indicateurs_alerte(donnees)
        }



simulateur = SimulateurLancement()
    
donnees_exemple = {
        "prix_vente": 100,
        "coût_production": 40,
        "coûts_fixes": 5000,
        "volume_mensuel": 150
    }
    
resultat = simulateur.executer_simulation(donnees_exemple)
        