from test import donnees_p1,donnees_p2

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

##############################################################################

def CA_produit(total_amount_product):
    """Calcule le CA pour un produit spécifique"""
    if not total_amount_product:
        return 0
    return sum(total_amount_product)

def Comparative_CA_produit(total_amount_product_p1, total_amount_product_p2, nom_produit=""):
    """Compare le CA d'un produit entre deux périodes"""
    CA_produit_p1 = CA_produit(total_amount_product_p1)
    CA_produit_p2 = CA_produit(total_amount_product_p2)
    
    if CA_produit_p1 == 0:
        variation_ca_produit = float('inf') if CA_produit_p2 > 0 else 0
    else:
        variation_ca_produit = round((CA_produit_p2 - CA_produit_p1) / CA_produit_p1 * 100, 2)
    
    return {
        "nom_produit": nom_produit,
        "CA_produit_p1": CA_produit_p1,
        "CA_produit_p2": CA_produit_p2,
        "variation_absolue": CA_produit_p2 - CA_produit_p1,
        "variation_pourcentage": variation_ca_produit
    }

def contribution_produit(total_amount_product_p1, total_amount_product_p2, 
                         liste_montant_transaction_p1, liste_montant_transaction_p2):
    """Calcule la contribution d'un produit à la variation totale du CA"""
    CA_produit_p1 = CA_produit(total_amount_product_p1)
    CA_produit_p2 = CA_produit(total_amount_product_p2)
    delta_ca_product = CA_produit_p2 - CA_produit_p1

    CA_total_p1 = CA(liste_montant_transaction_p1)
    CA_total_p2 = CA(liste_montant_transaction_p2)
    delta_ca_total = CA_total_p2 - CA_total_p1
    
    if delta_ca_total == 0:
        contribution_pourcentage = 0
    else:
        contribution_pourcentage = round((delta_ca_product / delta_ca_total) * 100, 2)
    
    # Catégorisation de la contribution
    if abs(contribution_pourcentage) >= 20:
        categorie = "Haute"
    elif abs(contribution_pourcentage) >= 5:
        categorie = "Moyenne"
    else:
        categorie = "Basse"
    
    return {
        "contribution_absolue": delta_ca_product,
        "contribution_pourcentage": contribution_pourcentage,
        "categorie": categorie,
        "impact": "positive" if delta_ca_product > 0 else "negative" if delta_ca_product < 0 else "neutre"
    }

def Ca_client(list_total_amount_client):
    """Calcule le CA total d'un client"""
    if not list_total_amount_client:
        return 0
    return sum(list_total_amount_client)

def panier_moyen(Ca_client, Nombre_commande):
    """Calcule le panier moyen d'un client"""
    if Nombre_commande == 0:
        return 0
    return Ca_client / Nombre_commande

def nombre_moyen_commande(Nombre_commande, Nombre_client_actif):
    """Calcule le nombre moyen de commandes par client"""
    if Nombre_client_actif == 0:
        return 0
    return Nombre_commande / Nombre_client_actif

def identifier_clients_vip(liste_ca_par_client, liste_frequence_par_client, 
                          liste_recence_par_client, top_percentile=20):
    """
    Identifie les clients VIP selon la méthode RFM (Récence, Fréquence, Montant)
    """
    if not liste_ca_par_client:
        return {}
    
    # Calcul des seuils
    ca_moyen = sum(liste_ca_par_client) / len(liste_ca_par_client)
    freq_moyenne = sum(liste_frequence_par_client) / len(liste_frequence_par_client) if liste_frequence_par_client else 0
    
    # Trouver le percentile pour le CA
    sorted_ca = sorted(liste_ca_par_client)
    index_percentile = int(len(sorted_ca) * top_percentile / 100)
    seuil_ca_vip = sorted_ca[-index_percentile] if index_percentile > 0 else sorted_ca[-1]
    
    clients_vip = []
    for i, ca in enumerate(liste_ca_par_client):
        est_vip = (
            ca >= seuil_ca_vip and  # Top X% en CA
            (liste_frequence_par_client[i] >= freq_moyenne if i < len(liste_frequence_par_client) else False) and
            (liste_recence_par_client[i] <= 30 if i < len(liste_recence_par_client) else False)  # Achat récent (≤ 30 jours)
        )
        if est_vip:
            clients_vip.append({
                "index": i,
                "CA": ca,
                "frequence": liste_frequence_par_client[i] if i < len(liste_frequence_par_client) else 0,
                "recence": liste_recence_par_client[i] if i < len(liste_recence_par_client) else 0
            })
    
    return {
        "nombre_vip": len(clients_vip),
        "seuil_ca_vip": seuil_ca_vip,
        "pourcentage_vip": round(len(clients_vip) / len(liste_ca_par_client) * 100, 2),
        "clients_vip": clients_vip
    }

###################################################################

def Ca_par_canal(liste_Tmontant_realiser_par_le_canal):
    """Calcule le CA pour un canal donné"""
    if not liste_Tmontant_realiser_par_le_canal:
        return 0
    return sum(liste_Tmontant_realiser_par_le_canal)

def Part_canal(liste_Tmontant_realiser_par_le_canal, CA_total_periode, nom_canal=""):
    """Calcule la part de marché d'un canal"""
    Ca_canal = Ca_par_canal(liste_Tmontant_realiser_par_le_canal)
    
    if CA_total_periode == 0:
        part_canal_ca = 0
    else:
        part_canal_ca = round((Ca_canal / CA_total_periode) * 100, 2)
    
    return {
        "canal": nom_canal,
        "CA_canal": Ca_canal,
        "part_marche": part_canal_ca
    }

def Variation_Ca_par_canal(liste_Tmontant_realiser_par_le_canal_p1, 
                          liste_Tmontant_realiser_par_le_canal_p2, 
                          nom_canal=""):
    """Calcule la variation du CA pour un canal"""
    Ca_p1 = Ca_par_canal(liste_Tmontant_realiser_par_le_canal_p1)
    Ca_p2 = Ca_par_canal(liste_Tmontant_realiser_par_le_canal_p2)
    
    if Ca_p1 == 0:
        variation_pourcentage = float('inf') if Ca_p2 > 0 else 0
    else:
        variation_pourcentage = round((Ca_p2 - Ca_p1) / Ca_p1 * 100, 2)
    
    # Contribution à la variation totale
    delta_ca_canal = Ca_p2 - Ca_p1
    
    return {
        "canal": nom_canal,
        "CA_p1": Ca_p1,
        "CA_p2": Ca_p2,
        "variation_absolue": delta_ca_canal,
        "variation_pourcentage": variation_pourcentage
    }

def analyse_globale_canaux(donnees_canaux_p1, donnees_canaux_p2, CA_total_p1, CA_total_p2):
    """
    Analyse globale de tous les canaux
    donnees_canaux = {
        "magasin": [montants...],
        "ecommerce": [montants...],
        "reseaux_sociaux": [montants...],
        "distributeurs": [montants...]
    }
    """
    resultats = {}
    delta_ca_total = CA_total_p2 - CA_total_p1
    
    for canal in donnees_canaux_p1.keys():
        if canal in donnees_canaux_p1 and canal in donnees_canaux_p2:
            # CA par canal
            ca_p1 = Ca_par_canal(donnees_canaux_p1[canal])
            ca_p2 = Ca_par_canal(donnees_canaux_p2[canal])
            
            # Part de marché
            part_p1 = Part_canal(donnees_canaux_p1[canal], CA_total_p1, canal)["part_marche"]
            part_p2 = Part_canal(donnees_canaux_p2[canal], CA_total_p2, canal)["part_marche"]
            
            # Variation
            variation = Variation_Ca_par_canal(donnees_canaux_p1[canal], donnees_canaux_p2[canal], canal)
            
            # Contribution
            delta_ca_canal = ca_p2 - ca_p1
            if delta_ca_total != 0:
                contribution = round((delta_ca_canal / delta_ca_total) * 100, 2)
            else:
                contribution = 0
            
            resultats[canal] = {
                "CA_p1": ca_p1,
                "CA_p2": ca_p2,
                "part_marche_p1": part_p1,
                "part_marche_p2": part_p2,
                "variation_absolue": delta_ca_canal,
                "variation_pourcentage": variation["variation_pourcentage"],
                "contribution": contribution,
                "evolution_part": round(part_p2 - part_p1, 2)
            }
    
    return resultats

####################################################################

def effet_Volume_p1_p2(Q_total_produit_p1, Q_total_produit_p2, CA_total_p1):
    """Calcule l'effet volume entre deux périodes"""
    if Q_total_produit_p1 == 0:
        return {"effet_volume": 0, "message": "Division par zéro"}
    
    prix_moyen_pondere = CA_total_p1 / Q_total_produit_p1
    effet_volume = (Q_total_produit_p2 - Q_total_produit_p1) * prix_moyen_pondere
    
    return {
        "effet_volume": round(effet_volume, 2),
        "prix_moyen_reference": round(prix_moyen_pondere, 2)
    }

def effet_prix_p1_p2(Q_total_produit_p1, Q_total_produit_p2, CA_total_p1, CA_total_p2):
    """Calcule l'effet prix entre deux périodes"""
    if Q_total_produit_p1 == 0 or Q_total_produit_p2 == 0:
        return {"effet_prix": 0, "message": "Division par zéro"}
    
    prix_moyen_pondere_p1 = CA_total_p1 / Q_total_produit_p1
    prix_moyen_pondere_p2 = CA_total_p2 / Q_total_produit_p2
    
    effet_prix = Q_total_produit_p1 * (prix_moyen_pondere_p2 - prix_moyen_pondere_p1)
    
    return {
        "effet_prix": round(effet_prix, 2),
        "prix_moyen_p1": round(prix_moyen_pondere_p1, 2),
        "prix_moyen_p2": round(prix_moyen_pondere_p2, 2)
    }

def effet_mix_p1_p2(Q_total_produit_p1, Q_total_produit_p2, CA_total_p1, CA_total_p2):
    """Calcule l'effet mix (effet croisé) entre deux périodes"""
    delta_ca = CA_total_p2 - CA_total_p1
    effet_volume = effet_Volume_p1_p2(Q_total_produit_p1, Q_total_produit_p2, CA_total_p1)["effet_volume"]
    effet_prix = effet_prix_p1_p2(Q_total_produit_p1, Q_total_produit_p2, CA_total_p1, CA_total_p2)["effet_prix"]
    
    effet_mix = delta_ca - (effet_volume + effet_prix)
    
    return {
        "effet_mix": round(effet_mix, 2),
        "delta_CA": round(delta_ca, 2),
        "effet_volume": round(effet_volume, 2),
        "effet_prix": round(effet_prix, 2)
    }

def decomposition_volume_prix(Q_total_produit_p1, Q_total_produit_p2, CA_total_p1, CA_total_p2):
    """Analyse complète de la décomposition volume/prix"""
    delta_ca = CA_total_p2 - CA_total_p1
    
    # Calcul des effets
    volume_effet = effet_Volume_p1_p2(Q_total_produit_p1, Q_total_produit_p2, CA_total_p1)["effet_volume"]
    prix_effet = effet_prix_p1_p2(Q_total_produit_p1, Q_total_produit_p2, CA_total_p1, CA_total_p2)["effet_prix"]
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

# Fonction utilitaire pour traiter une analyse complète
def analyse_comparative_complete(donnees_p1, donnees_p2):
    """
    Fonction principale pour une analyse complète
    donnees = {
        "montants": [liste des montants],
        "volumes": [liste des volumes],
        "clients": [liste des IDs clients],
        "canaux": {dict des canaux},
        "produits": {dict des produits}
    }
    """
    resultats = {}
    
    # Analyse globale
    resultats["ca"] = ComparativeCA_Kpi(donnees_p1["montants"], donnees_p2["montants"])
    resultats["volume"] = Comparative_Volume_Kpi(donnees_p1["volumes"], donnees_p2["volumes"])
    resultats["prix_moyen"] = Comparative_prix_moyen(
        resultats["ca"]["CA_p1"], resultats["volume"]["volume_p1"],
        resultats["ca"]["CA_p2"], resultats["volume"]["volume_p2"]
    )
    resultats["clients"] = client_actif(donnees_p1["clients"], donnees_p2["clients"])
    
    # Décomposition volume/prix
    resultats["decomposition"] = decomposition_volume_prix(
        resultats["volume"]["volume_p1"], resultats["volume"]["volume_p2"],
        resultats["ca"]["CA_p1"], resultats["ca"]["CA_p2"]
    )
    
    return resultats

result = analyse_comparative_complete(donnees_p1,donnees_p2)
