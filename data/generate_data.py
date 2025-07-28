import random
import datetime
import pandas as pd

# Définition des distributions pondérées selon la littérature médicale

# 1. Démographie
AGE_BINS = [(15, 29, 0.35), (30, 44, 0.20), (45, 59, 0.25), (60, 80, 0.20)]

# Sexe selon le type de maladie
SEX_BY_DIAG = {
    "Crohn": [("H", 0.48), ("F", 0.52)],
    "RCH": [("H", 0.50), ("F", 0.50)],
    "MICI": [("H", 0.49), ("F", 0.51)]  # Pour MICI indéterminée
}

# 2. Types de maladies (diagnostics)
DIAG_WEIGHTS = [
    ("Crohn iléo-colique", 0.24),  # 60% * 40%
    ("Crohn colique", 0.18),       # 60% * 30%
    ("Crohn iléal", 0.18),         # 60% * 30%
    ("RCH extensive", 0.14),       # 40% * 35%
    ("RCH distale", 0.26),         # 40% * 65%
    ("MICI indéterminée", 0.05)
]

# 3. Traitements adaptés selon le diagnostic
TREATMENTS_BY_DIAG = {
    "Crohn": [
        ("Infliximab", 0.25),
        ("Adalimumab", 0.30),
        ("Vedolizumab", 0.15),
        ("Ustekinumab", 0.15),
        ("Azathioprine", 0.14),
        ("Mesalazine", 0.01)  # Peu utilisé pour Crohn
    ],
    "RCH": [
        ("Infliximab", 0.30),
        ("Adalimumab", 0.20),
        ("Vedolizumab", 0.15),
        ("Ustekinumab", 0.05),
        ("Azathioprine", 0.15),
        ("Mesalazine", 0.15)  # Plus utilisé pour RCH
    ],
    "MICI": [  # Indéterminée
        ("Infliximab", 0.25),
        ("Adalimumab", 0.25),
        ("Vedolizumab", 0.15),
        ("Ustekinumab", 0.10),
        ("Azathioprine", 0.15),
        ("Mesalazine", 0.10)
    ]
}

# 4. Réponse au traitement selon la molécule
RESPONSE_BY_TREATMENT = {
    "Infliximab": [("Efficace", 0.60), ("Partiel", 0.25), ("Échec", 0.10), ("Rechute", 0.05)],
    "Adalimumab": [("Efficace", 0.55), ("Partiel", 0.25), ("Échec", 0.15), ("Rechute", 0.05)],
    "Vedolizumab": [("Efficace", 0.50), ("Partiel", 0.30), ("Échec", 0.15), ("Rechute", 0.05)],
    "Ustekinumab": [("Efficace", 0.45), ("Partiel", 0.30), ("Échec", 0.20), ("Rechute", 0.05)],
    "Azathioprine": [("Efficace", 0.45), ("Partiel", 0.30), ("Échec", 0.20), ("Rechute", 0.05)],
    "Mesalazine": [("Efficace", 0.64), ("Partiel", 0.25), ("Échec", 0.08), ("Rechute", 0.03)]
}

# 5. Effets indésirables par traitement
SIDE_EFFECTS_BY_TREATMENT = {
    "Infliximab": [
        ("Infections", 0.15), ("Céphalées", 0.10), ("Réactions Cutanées", 0.05), 
        ("Fatigue", 0.05), ("Douleurs articulaires", 0.03), ("Nausées", 0.02), ("Aucun", 0.60)
    ],
    "Adalimumab": [
        ("Infections", 0.12), ("Réactions Cutanées", 0.15), ("Céphalées", 0.08), 
        ("Fatigue", 0.04), ("Douleurs articulaires", 0.05), ("Aucun", 0.56)
    ],
    "Vedolizumab": [
        ("Infections", 0.08), ("Céphalées", 0.12), ("Fatigue", 0.10),
        ("Nausées", 0.07), ("Arthralgie", 0.03), ("Aucun", 0.60)
    ],
    "Ustekinumab": [
        ("Infections", 0.10), ("Céphalées", 0.08), ("Fatigue", 0.05),
        ("Nausées", 0.04), ("Douleurs articulaires", 0.03), ("Aucun", 0.70)
    ],
    "Azathioprine": [
        ("Nausées", 0.15), ("Fatigue", 0.10), ("Infections", 0.08),
        ("Douleurs abdominales", 0.07), ("Fièvre", 0.05), ("Aucun", 0.55)
    ],
    "Mesalazine": [
        ("Douleurs abdominales", 0.08), ("Nausées", 0.07), ("Céphalées", 0.05),
        ("Diarrhée", 0.03), ("Éruptions cutanées", 0.02), ("Aucun", 0.75)
    ]
}

# Fonction pour choisir une tranche d'âge spécifiquement
def choose_age_bin(bins):
    weights = [weight for _, _, weight in bins]
    index = random.choices(range(len(bins)), weights=weights, k=1)[0]
    return bins[index][0], bins[index][1]

# Fonction utilitaire pour le choix pondéré
def weighted_choice(pairs):
    """
    Effectue un choix pondéré parmi une liste de paires (élément, poids)
    """
    items, weights = zip(*pairs)
    return random.choices(items, weights=weights, k=1)[0]

def generate_patient_infos(patient_id):
    """
    Génère les informations de base pour un patient avec des distributions réalistes.
    """
    # Choix du diagnostic avec pondération
    maladie = weighted_choice(DIAG_WEIGHTS)
    
    # Détermination du type de maladie (Crohn, RCH ou MICI)
    if "Crohn" in maladie:
        type_maladie = "Crohn"
    elif "RCH" in maladie:
        type_maladie = "RCH"
    else:
        type_maladie = "MICI"
    
    # Choix du sexe selon le diagnostic
    sexe = weighted_choice(SEX_BY_DIAG[type_maladie])
    
    # Choix de la tranche d'âge puis de l'âge spécifique
    age_min, age_max = choose_age_bin(AGE_BINS)
    age = random.randint(age_min, age_max)
    
    # Ancienneté de la maladie (distribution triangulaire centrée sur 5-7 ans)
    max_anciennete = min(20, age - 15)  # Max 20 ans, mais pas plus que l'âge - 15 ans minimum
    if max_anciennete <= 0:
        anciennete = 1
    else:
        # Distribution triangulaire avec pic vers 5-7 ans
        mid_point = min(6, max_anciennete // 2)
        
        # Correction pour éviter l'erreur de range
        if mid_point < 1:
            anciennete = 1
        elif random.random() < 0.7:  # 70% des cas dans la première moitié
            anciennete = random.randint(1, mid_point)
        else:
            # Assurer que l'intervalle est valide
            start_range = mid_point + 1
            if start_range > max_anciennete:
                anciennete = max_anciennete
            else:
                anciennete = random.randint(start_range, max_anciennete)
    
    return {
        "id": patient_id,
        "age": age,
        "sexe": sexe,
        "maladie": maladie,
        "anciennete": anciennete
    }

def generate_consultation(patient):
    """
    Génère les données de consultation pour un patient donné avec des distributions réalistes.
    """
    # Date de consultation (0 à 20 ans en arrière, distribution triangulaire)
    today = datetime.date.today()
    if random.random() < 0.7:  # 70% des consultations dans les 5 dernières années
        days_ago = random.randint(0, 5 * 365)
    else:
        days_ago = random.randint(5 * 365, 20 * 365)
    date_consultation = today - datetime.timedelta(days=days_ago)
    
    # Déterminer le type de maladie pour la sélection du traitement
    if "Crohn" in patient["maladie"]:
        type_maladie = "Crohn"
    elif "RCH" in patient["maladie"]:
        type_maladie = "RCH"
    else:
        type_maladie = "MICI"
    
    # Sélection du traitement selon le type de maladie
    traitement = weighted_choice(TREATMENTS_BY_DIAG[type_maladie])
    
    # Sélection de la réponse au traitement
    reponse = weighted_choice(RESPONSE_BY_TREATMENT[traitement])
    
    # Sélection des effets secondaires
    effets_possibles = [effet for effet, _ in SIDE_EFFECTS_BY_TREATMENT[traitement] if effet != "Aucun"]
    
    # Probabilité d'avoir des effets secondaires (inverse du poids "Aucun")
    proba_effets = 1 - dict(SIDE_EFFECTS_BY_TREATMENT[traitement]).get("Aucun", 0)
    
    if random.random() < proba_effets and effets_possibles:
        # Nombre d'effets secondaires (1 à 3, pondéré vers 1)
        nb_effets = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
        nb_effets = min(nb_effets, len(effets_possibles))
        
        effets_secondaires = random.sample(
            population=effets_possibles,
            k=nb_effets
        )
    else:
        effets_secondaires = []
    
    return {
        "date_consultation": date_consultation.strftime("%d-%m-%Y"),
        "traitement": traitement,
        "effets_secondaires": ",".join(effets_secondaires),
        "reponse_traitement": reponse
    }

if __name__ == "__main__":
    data = []
    for i in range(1000):
        patient = generate_patient_infos(i + 1)
        consultation = generate_consultation(patient) 
        fusion = {**patient, **consultation}
        data.append(fusion)
    
    df = pd.DataFrame(data)
    
    # Vérification rapide de la distribution
    print("Distribution des maladies:")
    print(df["maladie"].value_counts(normalize=True))
    
    print("\nDistribution des traitements:")
    print(df["traitement"].value_counts(normalize=True))
    
    print("\nDistribution des réponses par traitement:")
    print(pd.crosstab(df["traitement"], df["reponse_traitement"], normalize="index"))
    
    # Sauvegarde du dataset
    df.to_csv("data/dataset.csv", index=False)
    print("\nSuccès! Dataset généré avec des distributions réalistes.")