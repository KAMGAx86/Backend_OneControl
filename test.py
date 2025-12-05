# STRUCTURE EXACTE POUR analyse_comparative_complete()
donnees_p1 = {
    # OBLIGATOIRE : pour ComparativeCA_Kpi()
    "montants": [150000, 200000, 75000, 300000, 50000, 120000, 180000, 220000],
    
    # OBLIGATOIRE : pour Comparative_Volume_Kpi()
    "volumes": [3, 5, 2, 12, 1, 3, 4, 6],
    
    # OBLIGATOIRE : pour client_actif()
    "clients": ["CUST-001", "CUST-002", "CUST-001", "CUST-003", "CUST-004", "CUST-005", "CUST-001", "CUST-002"],
    
    # OBLIGATOIRE : pour analyse_globale_canaux()
    "canaux": {
        "magasin": [150000, 200000, 180000, 220000],          # montants du canal magasin
        "ecommerce": [75000, 50000],                         # montants du canal ecommerce
        "reseaux_sociaux": [120000],                         # montants du canal réseaux sociaux
        "distributeurs": [300000]                            # montants du canal distributeurs
    },
    
    # OBLIGATOIRE : pour Comparative_CA_produit() et contribution_produit()
    "produits": {
        "RIZ-UB-25KG": [150000, 200000],                     # montants du produit Riz
        "HUILE-AZUR-5L": [75000],                            # montants du produit Huile
        "SAVON-CAMAY": [300000, 50000],                      # montants du produit Savon
        "LAIT-PEAK-400G": [120000],                          # montants du produit Lait
        "NESCAFE-CLASSIC": [180000, 220000]                  # montants du produit Café
    }
}

donnees_p2 = {
    # OBLIGATOIRE
    "montants": [180000, 220000, 90000, 350000, 60000, 140000, 160000, 190000],
    
    # OBLIGATOIRE
    "volumes": [4, 6, 3, 15, 2, 4, 5, 7],
    
    # OBLIGATOIRE
    "clients": ["CUST-001", "CUST-002", "CUST-004", "CUST-005", "CUST-006", "CUST-001", "CUST-003", "CUST-007"],
    
    # OBLIGATOIRE
    "canaux": {
        "magasin": [160000, 190000],                         # montants du canal magasin P2
        "ecommerce": [120000, 140000],                       # montants du canal ecommerce P2
        "reseaux_sociaux": [85000, 95000],                   # montants du canal réseaux sociaux P2
        "distributeurs": [350000, 60000]                     # montants du canal distributeurs P2
    },
    
    # OBLIGATOIRE
    "produits": {
        "RIZ-UB-25KG": [750000, 1000000],                    # montants du produit Riz P2
        "HUILE-AZUR-5L": [750000],                           # montants du produit Huile P2
        "SAVON-CAMAY": [200000, 55000],                      # montants du produit Savon P2
        "LAIT-PEAK-400G": [780000],                          # montants du produit Lait P2
        "NESCAFE-CLASSIC": [580000, 420000]                  # montants du produit Café P2
    }
}