import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def analyse_traitements(df):
    # --- 1. Titre et description ---
    st.title("📊 Analyse comparative des traitements")
    st.write(
        "Compare l'efficacité, la tolérance et la répartition des traitements dans différents sous-groupes de patients atteints de MICI. Utilise les filtres pour explorer les résultats selon l'âge, le sexe ou le type de maladie."
    )
    
    # --- 2. Section des filtres ---
    st.subheader("🔍 Filtres de population")
    col1, col2, col3 = st.columns(3)
    with col1:
        age_min, age_max = st.slider(
            "Tranche d'âge :", 
            min_value=int(df["age"].min()), 
            max_value=int(df["age"].max()), 
            value=(int(df["age"].min()), int(df["age"].max()))
        )
    with col2:
        sexes_disponibles = ["Tous"] + list(df["sexe"].unique())
        sexe_selectionne = st.selectbox("Sexe :", sexes_disponibles)
    with col3:
        maladies_disponibles = ["Toutes"] + list(df["maladie"].unique())
        maladie_selectionnee = st.selectbox("Type de MICI :", maladies_disponibles)
    
    # --- 3. Application des filtres ---
    df_filtre = df.copy()
    df_filtre = df_filtre[(df_filtre["age"] >= age_min) & (df_filtre["age"] <= age_max)]
    if sexe_selectionne != "Tous":
        df_filtre = df_filtre[df_filtre["sexe"] == sexe_selectionne]
    if maladie_selectionnee != "Toutes":
        df_filtre = df_filtre[df_filtre["maladie"] == maladie_selectionnee]
    
    # --- 4. Affichage des métriques dynamiques ---
    st.subheader("📈 Indicateurs pour la population filtrée")
    col1, col2, col3 = st.columns(3)
    col1.metric("Patients filtrés", len(df_filtre))
    col2.metric("Traitements concernés", df_filtre["traitement"].nunique())
    efficacite_moyenne = (df_filtre['reponse_traitement'] == 'Efficace').mean() * 100 if not df_filtre.empty else 0
    col3.metric("Efficacité moyenne", f"{efficacite_moyenne:.1f}%")
    st.info(f"Population filtrée : {len(df_filtre)} patients sur {len(df)} patients totaux")
    
    # Si aucun patient ne correspond aux critères, on arrête ici
    if df_filtre.empty:
        st.warning("Aucun patient ne correspond aux critères sélectionnés. Veuillez modifier les filtres.")
        return

    # --- 5. Calculs et graphiques basés sur les données filtrées ---
    
    # Calculer l'efficacité pour chaque traitement
    resultats_par_traitement = []
    for traitement in df_filtre["traitement"].unique():
        df_traitement = df_filtre[df_filtre["traitement"] == traitement]
        nb_patients = len(df_traitement)
        taux_efficacite = (df_traitement["reponse_traitement"] == "Efficace").mean() * 100
        taux_echec = (df_traitement["reponse_traitement"] == "Échec").mean() * 100
        effets_secondaires = df_traitement["effets_secondaires"].str.len() > 0
        taux_effets = effets_secondaires.mean() * 100
        resultats_par_traitement.append({
            "traitement": traitement,
            "patients": nb_patients,
            "taux_efficacite": taux_efficacite,
            "taux_echec": taux_echec,
            "taux_effets": taux_effets
        })
    df_resultats = pd.DataFrame(resultats_par_traitement)
    
    # Comparaison principale - Graphique à barres horizontal
    st.subheader("🎯 Comparaison de l'efficacité des traitements")
    df_resultats = df_resultats.sort_values("taux_efficacite", ascending=False)
    fig = px.bar(
        df_resultats,
        y="traitement",
        x="taux_efficacite",
        orientation="h",
        text=df_resultats["taux_efficacite"].round(1).astype(str) + " %",
        color="taux_efficacite",
        color_continuous_scale=["red", "yellow", "green"],
        labels={"traitement": "Traitement", "taux_efficacite": "Taux d'efficacité (%)"},
        title="Efficacité des traitements (%)",
        hover_data=["patients"]
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau de synthèse
    st.subheader("📋 Tableau de synthèse des traitements")
    df_tableau = df_resultats.rename(columns={
        "traitement": "Traitement",
        "patients": "Patients",
        "taux_efficacite": "Efficacité (%)",
        "taux_echec": "Échec (%)",
        "taux_effets": "Effets secondaires (%)"
    }).round(1)
    st.dataframe(
        df_tableau.set_index("Traitement"),
        use_container_width=True,
        hide_index=False
    )
    
    # Visualisation secondaire - Distribution des réponses
    st.subheader("📊 Distribution des réponses par traitement")
    resultats_complets = []
    for traitement in df_filtre["traitement"].unique():
        df_traitement = df_filtre[df_filtre["traitement"] == traitement]
        for reponse in ["Efficace", "Partiel", "Échec", "Rechute"]:
            count = (df_traitement["reponse_traitement"] == reponse).sum()
            pourcentage = (count / len(df_traitement)) * 100 if len(df_traitement) > 0 else 0
            resultats_complets.append({
                "traitement": traitement,
                "reponse": reponse,
                "count": count,
                "pourcentage": pourcentage
            })
    df_reponses = pd.DataFrame(resultats_complets)
    fig2 = px.bar(
        df_reponses,
        x="traitement",
        y="pourcentage",
        color="reponse",
        color_discrete_map={
            "Efficace": "green",
            "Partiel": "blue",
            "Rechute": "orange",
            "Échec": "red"
        },
        text=df_reponses["pourcentage"].round(1).astype(str) + "%",
        title="Distribution des réponses aux traitements (%)",
        labels={"traitement": "Traitement", "pourcentage": "Pourcentage (%)", "reponse": "Réponse"}
    )
    fig2.update_traces(textposition="inside", textfont_size=10)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Analyse des effets secondaires
    st.subheader("⚠️ Principaux effets secondaires par traitement")
    tous_effets = []
    for effets in df_filtre["effets_secondaires"].dropna():
        if effets:
            effets_liste = effets.split(',')
            tous_effets.extend([effet.strip() for effet in effets_liste])
    
    if tous_effets:
        effets_counts = pd.Series(tous_effets).value_counts().head(10)
        fig3 = px.bar(
            x=effets_counts.values,
            y=effets_counts.index,
            orientation="h",
            text=effets_counts.values,
            title="Top 10 des effets secondaires signalés",
            labels={"x": "Nombre de signalements", "y": "Effet secondaire"}
        )
        fig3.update_traces(textposition="outside")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Aucun effet secondaire à afficher pour la population filtrée.")

    # Insights automatiques
    st.subheader("💡 Points clés à retenir")
    if not df_resultats.empty:
        traitement_efficace = df_resultats.iloc[0]["traitement"]
        taux_efficacite_max = df_resultats.iloc[0]["taux_efficacite"]
        traitement_moins_efficace = df_resultats.iloc[-1]["traitement"]
        taux_efficacite_min = df_resultats.iloc[-1]["taux_efficacite"]
        nb_patients_filtre = len(df_filtre)
        
        st.info(
            f"""
            **Analyse pour {nb_patients_filtre} patients :**
            
            * Le traitement le plus efficace est **{traitement_efficace}** avec un taux de {taux_efficacite_max:.1f}% d'efficacité.
            * Le traitement le moins efficace est **{traitement_moins_efficace}** avec un taux de {taux_efficacite_min:.1f}% d'efficacité.
            * La différence d'efficacité entre les deux est de **{taux_efficacite_max - taux_efficacite_min:.1f} points**.
            
            **Suggestion d'analyse :** Examiner les caractéristiques des patients pour lesquels {traitement_efficace} a été le plus efficace.
            """
        )
    else:
        st.info("Données insuffisantes pour générer des insights.")