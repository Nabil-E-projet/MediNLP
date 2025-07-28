import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def pharmacovigilance(df):
    # Titre et description
    st.title("⚠️ Pharmacovigilance et tolérance")
    st.write(
        "Analyse des effets secondaires rapportés pour les différents traitements des MICI. "
        "Cette page aide à identifier les risques associés aux médicaments et les profils à risque."
    )
    
    # Préparation des données d'effets secondaires
    # On crée une liste de tous les effets secondaires signalés
    tous_effets = []
    patients_avec_effets = 0
    
    for idx, row in df.iterrows():
        effets = row["effets_secondaires"]
        if isinstance(effets, str) and effets.strip():  # Vérifier que ce n'est pas vide
            effets_liste = effets.split(',')
            tous_effets.extend([effet.strip() for effet in effets_liste])
            patients_avec_effets += 1
    
    # Métriques principales
    col1, col2, col3 = st.columns(3)
    col1.metric("Effets secondaires signalés", len(tous_effets))
    col2.metric("Patients avec effets secondaires", patients_avec_effets)
    col3.metric("% patients avec effets", f"{patients_avec_effets/len(df)*100:.1f}%")
    
    # Section des filtres
    st.subheader("🔍 Filtres")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtre par traitement
        traitements_disponibles = ["Tous"] + sorted(df["traitement"].unique().tolist())
        traitement_selectionne = st.selectbox("Traitement :", traitements_disponibles)
    
    with col2:
        # Filtre par sexe du patient
        sexes_disponibles = ["Tous"] + sorted(df["sexe"].unique().tolist())
        sexe_selectionne = st.selectbox("Sexe du patient :", sexes_disponibles)
    
    # Application des filtres
    df_filtre = df.copy()
    
    if traitement_selectionne != "Tous":
        df_filtre = df_filtre[df_filtre["traitement"] == traitement_selectionne]
    
    if sexe_selectionne != "Tous":
        df_filtre = df_filtre[df_filtre["sexe"] == sexe_selectionne]
    
    st.info(f"Population filtrée : {len(df_filtre)} patients sur {len(df)} patients totaux")
    
    # Top 10 des effets secondaires (global ou filtré)
    st.subheader("📊 Top effets secondaires")
    
    # Recalculer les effets secondaires pour la population filtrée
    effets_filtres = []
    for effets in df_filtre["effets_secondaires"].dropna():
        if isinstance(effets, str) and effets.strip():
            effets_liste = effets.split(',')
            effets_filtres.extend([effet.strip() for effet in effets_liste])
    
    # Compter les occurrences
    if effets_filtres:
        effets_counts = pd.Series(effets_filtres).value_counts().head(10)
        
        # Créer le graphique à barres horizontales
        fig1 = px.bar(
            x=effets_counts.values,
            y=effets_counts.index,
            orientation="h",
            labels={"x": "Nombre de signalements", "y": "Effet secondaire"},
            title="Top 10 des effets secondaires signalés",
            color=effets_counts.values,
            color_continuous_scale=["yellow", "orange", "red"]
        )
        fig1.update_traces(texttemplate="%{x}", textposition="outside")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("Aucun effet secondaire signalé pour les filtres sélectionnés.")
    
    # Carte de chaleur des effets secondaires par traitement
    st.subheader("🔥 Distribution des effets par traitement")
    
    # Créer un DataFrame pour la heatmap
    effets_par_traitement = {}
    
    for traitement in df["traitement"].unique():
        effets_traitement = []
        for effets in df[df["traitement"] == traitement]["effets_secondaires"].dropna():
            if isinstance(effets, str) and effets.strip():
                effets_liste = effets.split(',')
                effets_traitement.extend([effet.strip() for effet in effets_liste])
        
        # Compter les occurrences pour ce traitement
        if effets_traitement:
            counts = pd.Series(effets_traitement).value_counts()
            effets_par_traitement[traitement] = counts
    
    # Construire le DataFrame pour la heatmap
    if effets_par_traitement:
        # Récupérer tous les effets uniques
        tous_effets_uniques = set()
        for counts in effets_par_traitement.values():
            tous_effets_uniques.update(counts.index)
        
        # Initialiser le DataFrame avec des zéros
        heatmap_data = pd.DataFrame(0, 
                                   index=list(effets_par_traitement.keys()),
                                   columns=sorted(list(tous_effets_uniques)))
        
        # Remplir avec les nombres réels
        for traitement, counts in effets_par_traitement.items():
            for effet, count in counts.items():
                heatmap_data.loc[traitement, effet] = count
        
        # Sélectionner les 10 effets les plus courants pour la lisibilité
        top_effets = pd.Series(tous_effets).value_counts().head(10).index.tolist()
        heatmap_data_filtre = heatmap_data[top_effets]
        
        # Créer la heatmap
        fig2 = px.imshow(
            heatmap_data_filtre.values,
            x=top_effets,
            y=heatmap_data_filtre.index,
            labels=dict(x="Effet secondaire", y="Traitement", color="Fréquence"),
            color_continuous_scale="Reds",
            title="Fréquence des effets secondaires par traitement"
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Données insuffisantes pour créer la carte de chaleur.")
    
    # Tableau détaillé des effets secondaires
    st.subheader("📋 Détail des effets secondaires")
    
    # Créer un DataFrame pour le tableau
    tableau_effets = []
    
    for traitement in df["traitement"].unique():
        df_traitement = df[df["traitement"] == traitement]
        
        # Collecter tous les effets pour ce traitement
        effets_traitement = []
        for effets in df_traitement["effets_secondaires"].dropna():
            if isinstance(effets, str) and effets.strip():
                effets_liste = effets.split(',')
                effets_traitement.extend([effet.strip() for effet in effets_liste])
        
        if effets_traitement:
            # Compter les occurrences
            effets_counts = pd.Series(effets_traitement).value_counts()
            
            # Calculer les pourcentages
            total_patients = len(df_traitement)
            
            for effet, count in effets_counts.items():
                tableau_effets.append({
                    "Traitement": traitement,
                    "Effet secondaire": effet,
                    "Nombre de cas": count,
                    "% des patients": f"{count/total_patients*100:.1f}%"
                })
    
    # Afficher le tableau
    if tableau_effets:
        df_tableau = pd.DataFrame(tableau_effets)
        st.dataframe(df_tableau, use_container_width=True)
    else:
        st.warning("Aucune donnée disponible pour le tableau.")
    
    # Conclusion et insights
    st.subheader("💡 Points clés à retenir")
    
    # Trouver le traitement avec le plus d'effets secondaires
    if effets_par_traitement:
        effets_totaux_par_traitement = {traitement: sum(counts) 
                                      for traitement, counts in effets_par_traitement.items()}
        traitement_plus_effets = max(effets_totaux_par_traitement, 
                                  key=effets_totaux_par_traitement.get)
        
        # Trouver l'effet secondaire le plus fréquent
        tous_effets_series = pd.Series(tous_effets)
        effet_plus_frequent = tous_effets_series.value_counts().index[0] if len(tous_effets_series) > 0 else "Aucun"
        
        st.info(
            f"""
            **Analyse de pharmacovigilance :**
            
            * Le traitement avec le plus d'effets secondaires signalés est **{traitement_plus_effets}**.
            * L'effet secondaire le plus fréquemment rapporté est **{effet_plus_frequent}**.
            * **{patients_avec_effets}** patients ({patients_avec_effets/len(df)*100:.1f}%) ont signalé au moins un effet secondaire.
            
            **Recommandation :** Un suivi particulier des patients sous {traitement_plus_effets} 
            pourrait être nécessaire, avec une attention particulière aux symptômes de {effet_plus_frequent}.
            """
        )
    else:
        st.info("Données insuffisantes pour générer des insights.")