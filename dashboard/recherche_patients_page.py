import streamlit as st
import pandas as pd
import plotly.express as px

def recherche_patients(df):
    # Titre et description
    st.title("🔍 Recherche de patients")
    st.write(
        "Outil de recherche avancée pour identifier des patients selon des critères multiples. "
        "Permet de trouver des profils similaires et d'explorer des cas cliniques spécifiques."
    )
    
    # Compteur global
    st.info(f"Base de données: {len(df)} patients au total")
    
    # Création des filtres en colonnes
    st.subheader("📋 Critères de recherche")
    
    # Première ligne de filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Filtre par âge
        age_min, age_max = st.slider(
            "Âge :", 
            min_value=int(df["age"].min()), 
            max_value=int(df["age"].max()), 
            value=(int(df["age"].min()), int(df["age"].max()))
        )
    
    with col2:
        # Filtre par sexe
        sexes_disponibles = ["Tous"] + list(df["sexe"].unique())
        sexe_selectionne = st.selectbox("Sexe :", sexes_disponibles)
    
    with col3:
        # Filtre par type de MICI
        maladies_disponibles = ["Toutes"] + list(df["maladie"].unique())
        maladie_selectionnee = st.selectbox("Type de MICI :", maladies_disponibles)
    
    # Deuxième ligne de filtres
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtre par traitement
        traitements_disponibles = ["Tous"] + sorted(df["traitement"].unique().tolist())
        traitement_selectionne = st.selectbox("Traitement :", traitements_disponibles)
    
    with col2:
        # Filtre par réponse au traitement
        reponses_disponibles = ["Toutes"] + sorted(df["reponse_traitement"].unique().tolist())
        reponse_selectionnee = st.selectbox("Réponse au traitement :", reponses_disponibles)
    
    # Application des filtres
    df_filtre = df.copy()
    df_filtre = df_filtre[(df_filtre["age"] >= age_min) & (df_filtre["age"] <= age_max)]
    
    if sexe_selectionne != "Tous":
        df_filtre = df_filtre[df_filtre["sexe"] == sexe_selectionne]
    
    if maladie_selectionnee != "Toutes":
        df_filtre = df_filtre[df_filtre["maladie"] == maladie_selectionnee]
    
    if traitement_selectionne != "Tous":
        df_filtre = df_filtre[df_filtre["traitement"] == traitement_selectionne]
    
    if reponse_selectionnee != "Toutes":
        df_filtre = df_filtre[df_filtre["reponse_traitement"] == reponse_selectionnee]
    
    # Afficher le nombre de résultats
    nb_resultats = len(df_filtre)
    if nb_resultats > 0:
        st.success(f"✅ {nb_resultats} patients correspondent aux critères de recherche")
    else:
        st.error("❌ Aucun patient ne correspond aux critères sélectionnés")
        st.stop()
    
    # Profil du groupe sélectionné
    st.subheader("📊 Profil du groupe sélectionné")
    col1, col2, col3 = st.columns(3)
    
    age_moyen = df_filtre["age"].mean()
    col1.metric("Âge moyen", f"{age_moyen:.1f} ans")
    
    nb_hommes = (df_filtre["sexe"] == "H").sum()
    nb_femmes = (df_filtre["sexe"] == "F").sum()
    col2.metric("Hommes / Femmes", f"{nb_hommes} / {nb_femmes}")
    
    taux_efficacite = (df_filtre["reponse_traitement"] == "Efficace").mean() * 100
    col3.metric("Taux d'efficacité", f"{taux_efficacite:.1f}%")
    
    # Graphiques d'analyse du groupe
    col1, col2 = st.columns(2)
    with col1:
        if len(df_filtre["maladie"].unique()) > 1:
            fig1 = px.pie(
                df_filtre, 
                names="maladie",
                title="Répartition par type de MICI"
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info(f"Tous les patients ont la maladie: {df_filtre['maladie'].iloc[0]}")
    
    with col2:
        fig2 = px.pie(
            df_filtre,
            names="reponse_traitement",
            title="Réponses aux traitements",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Liste des patients
    st.subheader("👥 Liste des patients")
    colonnes_a_afficher = ["id", "age", "sexe", "maladie", "traitement", "reponse_traitement"]
    st.dataframe(
        df_filtre[colonnes_a_afficher],
        use_container_width=True,
        hide_index=True
    )
    
    # Option pour voir les détails
    with st.expander("Voir les détails complets"):
        st.dataframe(df_filtre, use_container_width=True)
    
    # Export en PDF (plus professionnel et préserve les caractères spéciaux)
    st.subheader("📄 Exporter les résultats")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Garder l'option CSV pour compatibilité
        csv = df_filtre.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📥 Télécharger CSV",
            data=csv,
            file_name="patients_filtres.csv",
            mime="text/csv"
        )
    
    with col2:
        # Générer un rapport PDF basique avec HTML
        from io import StringIO
        import base64
        
        # Créer une représentation HTML pour PDF
        html_string = f"""
        <h2>Rapport de recherche patients - MediNLP</h2>
        <p>Date d'extraction : {pd.Timestamp.now().strftime('%d/%m/%Y')}</p>
        <p><b>{nb_resultats} patients correspondent aux critères</b></p>
        <hr>
        {df_filtre[colonnes_a_afficher].to_html(index=False)}
        <hr>
        <p><i>Dashboard MediNLP - Projet FORECAST MICI</i></p>
        """
        
        # Encoder en base64 pour le téléchargement
        b64 = base64.b64encode(html_string.encode()).decode()
        
        st.download_button(
            label="📄 Télécharger rapport",
            data=html_string,
            file_name="rapport_patients.html",
            mime="text/html"
        )
        
        st.caption("💡 Le rapport HTML peut être imprimé en PDF depuis votre navigateur")
    
    # Informations complémentaires sur la cohorte
    st.subheader("💡 Cas similaires")
    st.info(
        f"""
        **Analyse de la cohorte filtrée :**
        
        * {nb_resultats} patients correspondent aux critères sélectionnés ({nb_resultats/len(df)*100:.1f}% de la base)
        * Âge moyen: {age_moyen:.1f} ans (min: {df_filtre['age'].min()}, max: {df_filtre['age'].max()})
        * Répartition par sexe: {nb_hommes} hommes ({nb_hommes/nb_resultats*100:.1f}%) et {nb_femmes} femmes ({nb_femmes/nb_resultats*100:.1f}%)
        * Traitement principal: {df_filtre['traitement'].value_counts().index[0]} ({df_filtre['traitement'].value_counts().iloc[0]} patients)
        
        Cette cohorte peut être utilisée pour des analyses plus approfondies ou pour identifier des profils spécifiques.
        """
    )