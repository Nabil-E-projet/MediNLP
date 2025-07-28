import streamlit as st
import pandas as pd
import plotly.express as px
import random

def aide_decision(df):
    # Titre avec emoji
    st.title("🧠 Aide à la décision thérapeutique")
    
    # Description simple
    st.write(
        "Cet outil simule un système d'aide à la décision pour les traitements MICI. "
        "Entrez les informations du patient pour recevoir une suggestion de traitement."
    )
    
    # Encadré bleu d'information
    st.info("Les recommandations sont basées sur l'analyse des patients similaires dans la base de données.")
    
    # Création de deux colonnes pour le formulaire
    col1, col2 = st.columns(2)
    
    # Première colonne - Informations de base
    with col1:
        st.subheader("Informations du patient")
        # Utilisation de widgets simples
        age = st.slider("Âge du patient", 18, 90, 45)
        sexe = st.radio("Sexe", ["H", "F"])
        
    # Deuxième colonne - Informations sur la maladie
    with col2:
        st.subheader("Caractéristiques de la maladie")
        # Liste déroulante simple
        maladie = st.selectbox("Type de MICI", options=df["maladie"].unique())
        # Checkbox pour options supplémentaires
        severe = st.checkbox("Forme sévère")
    
    # Séparateur visuel
    st.markdown("---")
    
    # Bouton d'action principal
    if st.button("Générer une recommandation de traitement", use_container_width=True):
        
        # Animation de chargement
        with st.spinner("Analyse en cours..."):
            # Simulation d'un petit délai pour donner l'impression de calcul
            import time
            time.sleep(1.5)
            
            # Filtrage basique des patients similaires
            patients_similaires = df[
                (df["sexe"] == sexe) & 
                (df["maladie"] == maladie)
            ]
            
            # Comptage simple des résultats par traitement
            resultats = {}
            for traitement in patients_similaires["traitement"].unique():
                patients_traitement = patients_similaires[patients_similaires["traitement"] == traitement]
                # Calcul simple d'efficacité 
                efficacite = (patients_traitement["reponse_traitement"] == "Efficace").mean() * 100
                resultats[traitement] = {
                    "efficacite": efficacite,
                    "patients": len(patients_traitement)
                }
        
        # Affichage des résultats
        if resultats:
            # Transformation en DataFrame pour faciliter le tri
            resultats_df = pd.DataFrame([
                {"traitement": t, "efficacite": r["efficacite"], "patients": r["patients"]} 
                for t, r in resultats.items()
            ])
            
            # Tri par efficacité
            resultats_df = resultats_df.sort_values("efficacite", ascending=False)
            
            # Recommandation principale
            meilleur_traitement = resultats_df.iloc[0]["traitement"]
            meilleure_efficacite = resultats_df.iloc[0]["efficacite"]
            
            # Affichage de la recommandation dans un encadré vert
            st.success(f"""
                ### Traitement recommandé: **{meilleur_traitement}**
                
                Pour un patient de {age} ans, {sexe}, avec {maladie}
                
                * Taux de réussite estimé: **{meilleure_efficacite:.1f}%**
                * Basé sur {resultats_df.iloc[0]["patients"]} cas similaires
            """)
            
            # Graphique simple pour visualiser les options
            st.subheader("Comparaison des traitements")
            fig = px.bar(
                resultats_df,
                x="traitement", 
                y="efficacite",
                color="efficacite",
                color_continuous_scale=["red", "yellow", "green"],
                labels={"traitement": "Traitement", "efficacite": "Efficacité (%)"}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tableau simple
            st.subheader("Détails")
            st.dataframe(
                resultats_df.rename(columns={
                    "traitement": "Traitement", 
                    "efficacite": "Efficacité (%)", 
                    "patients": "Nombre de patients"
                }).round(1)
            )
            
        else:
            # Message d'erreur simple
            st.error("Pas assez de données pour ce profil de patient.")
            
