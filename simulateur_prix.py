def actuel_CA(prix_actuel, volume_actuel):
    
    return prix_actuel * volume_actuel

def variation_prix(prix_nouveau, prix_actuel):
    
    return ((prix_nouveau - prix_actuel) / prix_actuel) * 100

def volume_requis(prix_actuel, volume_actuel, prix_nouveau):
    
    ca_actuel = actuel_CA(prix_actuel, volume_actuel)
    volume_requis = ca_actuel / prix_nouveau
    variation_volume_requis = volume_requis - volume_actuel
    return volume_requis, variation_volume_requis

def volume_estime(volume_actuel, variation_prix, elasticite=1.2):
    
    variation_volume_pct = -elasticite * (variation_prix / 100)
    volume_estime = volume_actuel * (1 + variation_volume_pct)
    return volume_estime

def nouveau_CA(prix_nouveau, volume_estime):

    return prix_nouveau * volume_estime

def variation_CA(ca_nouveau, ca_actuel):

    return ((ca_nouveau - ca_actuel) / ca_actuel) * 100

def simulation_complete(prix_actuel, volume_actuel, prix_nouveau, elasticite=1.2):

    
    ca_actuel = actuel_CA(prix_actuel, volume_actuel)
    
    var_prix = variation_prix(prix_nouveau, prix_actuel)
    
    vol_requis, var_vol_requis = volume_requis(prix_actuel, volume_actuel, prix_nouveau)
    
    vol_estime = volume_estime(volume_actuel, var_prix, elasticite)
    
    ca_nouveau = nouveau_CA(prix_nouveau, vol_estime)

    var_ca = variation_CA(ca_nouveau, ca_actuel)
    
    var_vol_estime_pct = ((vol_estime - volume_actuel) / volume_actuel) * 100 if volume_actuel != 0 else 0
    
    return {
        "prix_nouveau": prix_nouveau,
        "variation_prix_pct": var_prix,
        "ca_actuel": ca_actuel,
        "volume_requis": vol_requis,
        "variation_volume_requis": var_vol_requis,
        "volume_estime": vol_estime,
        "variation_volume_estime_pct": var_vol_estime_pct,
        "ca_nouveau": ca_nouveau,
        "variation_ca_pct": var_ca
    }


donnees_simulation = {
    "prix_actuel" : 5000,
    "volume_actuel" : 100,
    "prix_nouveau" : 4250
}
    
resultats_simulaton_prix = simulation_complete(donnees_simulation["prix_actuel"], donnees_simulation["volume_actuel"], donnees_simulation["prix_nouveau"])

    