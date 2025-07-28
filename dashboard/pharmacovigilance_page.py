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

    # --- 1. Section des filtres ---
    st.subheader("🔍 Filtres")
    col1, col2 = st.columns(2)
    with col1:
        traitements_disponibles = ["Tous"] + sorted(df["traitement"].unique().tolist())
        traitement_selectionne = st.selectbox("Traitement :", traitements_disponibles)
    with col2:
        sexes_disponibles = ["Tous"] + sorted(df["sexe"].unique().tolist())
        sexe_selectionne = st.selectbox("Sexe du patient :", sexes_disponibles)

    # --- 2. Application des filtres ---
    df_filtre = df.copy()
    if traitement_selectionne != "Tous":
        df_filtre = df_filtre[df_filtre["traitement"] == traitement_selectionne]
    if sexe_selectionne != "Tous":
        df_filtre = df_filtre[df_filtre["sexe"] == sexe_selectionne]

    # --- 3. Calculs basés sur les données filtrées ---
    effets_filtres = []
    patients_avec_effets = 0
    for idx, row in df_filtre.iterrows():
        effets = row["effets_secondaires"]
        if isinstance(effets, str) and effets.strip():
            effets_liste = effets.split(',')
            effets_filtres.extend([effet.strip() for effet in effets_liste])
            patients_avec_effets += 1

    # --- 4. Affichage des métriques dynamiques ---
    st.subheader("📈 Indicateurs pour la population filtrée")
    col1, col2, col3 = st.columns(3)
    col1.metric("Effets secondaires signalés", len(effets_filtres))
    col2.metric("Patients avec effets secondaires", patients_avec_effets)
    pourcentage_effets = (patients_avec_effets / len(df_filtre) * 100) if not df_filtre.empty else 0
    col3.metric("% patients avec effets", f"{pourcentage_effets:.1f}%")
    st.info(f"Population filtrée : {len(df_filtre)} patients sur {len(df)} patients totaux")

    # Si aucun patient ne correspond aux critères, on arrête ici
    if df_filtre.empty:
        st.warning("Aucun patient ne correspond aux critères sélectionnés. Veuillez modifier les filtres.")
        return

    # --- 5. Graphiques et tableaux dynamiques ---

    # Top 10 des effets secondaires
    st.subheader("📊 Top effets secondaires")
    if effets_filtres:
        effets_counts = pd.Series(effets_filtres).value_counts().head(10)
        fig1 = px.bar(
            x=effets_counts.values,
            y=effets_counts.index,
            orientation="h",
            labels={"x": "Nombre de signalements", "y": "Effet secondaire"},
            title="Top 10 des effets secondaires signalés",
            color=effets_counts.values,
            color_continuous_scale="Reds"
        )
        fig1.update_layout(yaxis={'categoryorder':'total ascending'})
        fig1.update_traces(texttemplate="%{x}", textposition="outside")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Aucun effet secondaire signalé pour les filtres sélectionnés.")

    # Carte de chaleur des effets secondaires par traitement
    st.subheader("🔥 Distribution des effets par traitement")
    effets_par_traitement = {}
    for traitement in df_filtre["traitement"].unique():
        df_traitement_specifique = df_filtre[df_filtre["traitement"] == traitement]
        effets_traitement = []
        for effets in df_traitement_specifique["effets_secondaires"].dropna():
            if isinstance(effets, str) and effets.strip():
                effets_traitement.extend([e.strip() for e in effets.split(',')])
        if effets_traitement:
            effets_par_traitement[traitement] = pd.Series(effets_traitement).value_counts()

    if effets_par_traitement:
        heatmap_df = pd.DataFrame(effets_par_traitement).fillna(0).astype(int)
        top_effets = pd.Series(effets_filtres).value_counts().head(10).index
        heatmap_df_filtre = heatmap_df.loc[heatmap_df.index.isin(top_effets)]
        
        if not heatmap_df_filtre.empty:
            fig2 = px.imshow(
                heatmap_df_filtre.T,
                labels=dict(x="Effet secondaire", y="Traitement", color="Fréquence"),
                color_continuous_scale="Reds",
                title="Fréquence des effets secondaires par traitement"
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Pas assez de données pour afficher la distribution.")
    else:
        st.info("Aucune donnée d'effet secondaire pour créer la carte de chaleur.")

    # Tableau détaillé des effets secondaires
    st.subheader("📋 Détail des effets secondaires")
    tableau_effets = []
    for traitement in df_filtre["traitement"].unique():
        df_traitement = df_filtre[df_filtre["traitement"] == traitement]
        total_patients = len(df_traitement)
        effets_traitement_str = df_traitement["effets_secondaires"].dropna()
        
        if not effets_traitement_str.empty:
            effets_liste = [e.strip() for effets in effets_traitement_str for e in effets.split(',')]
            effets_counts = pd.Series(effets_liste).value_counts()
            
            for effet, count in effets_counts.items():
                tableau_effets.append({
                    "Traitement": traitement,
                    "Effet secondaire": effet,
                    "Nombre de cas": count,
                    "% des patients du groupe": f"{count/total_patients*100:.1f}%"
                })

    if tableau_effets:
        df_tableau = pd.DataFrame(tableau_effets)
        st.dataframe(df_tableau, use_container_width=True)
    else:
        st.info("Aucune donnée disponible pour le tableau détaillé.")

    # Conclusion et insights
    st.subheader("💡 Points clés à retenir")
    if effets_par_traitement:
        effets_totaux_par_traitement = {t: v.sum() for t, v in effets_par_traitement.items()}
        traitement_plus_effets = max(effets_totaux_par_traitement, key=effets_totaux_par_traitement.get)
        effet_plus_frequent = pd.Series(effets_filtres).value_counts().index[0]

        st.info(
            f"""
            **Analyse de la population filtrée :**
            - Le traitement avec le plus d'effets secondaires signalés est **{traitement_plus_effets}**.
            - L'effet secondaire le plus fréquent est **{effet_plus_frequent}**.
            - **{patients_avec_effets}** patients ({pourcentage_effets:.1f}%) ont signalé au moins un effet secondaire.
            """
        )
    else:
        st.info("Données insuffisantes pour générer des insights.")