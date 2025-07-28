import pandas as pd
import streamlit as st
import plotly.express as px
from traitements_page import traitements  
from analyse_comparative_page import analyse_traitements
from pharmacovigilance_page import pharmacovigilance
from recherche_patients_page import recherche_patients
from aide_decision_page import aide_decision
from extraction_nlp_page import extraction_nlp

st.set_page_config(
    page_title="MediNLP - Accueil",
    page_icon="🏠",
    layout="wide"
)

st.sidebar.title("🩺 Dashboard MediNLP")
st.sidebar.markdown("---")

pages = [
    "🏠 Accueil",
    "💊 Traitements",
    "📊 Analyse comparative",
    "⚠️ Pharmacovigilance",
    "🔍 Recherche patients",
    "🧠 Aide à la décision",
    "🔍 Extraction NLP"



]

selected_page = st.sidebar.selectbox("Navigation", pages)

df = pd.read_csv("data/dataset.csv")

if selected_page == "🏠 Accueil":
    st.title("🏥 MediNLP - Analyse des MICI")
    st.write(
        "Bienvenue sur MediNLP, le dashboard interactif d'analyse pharmaco-épidémiologique des MICI "
        "(Maladie de Crohn & Rectocolite hémorragique). "
        "Ce système permet de visualiser et comparer les traitements et leurs effets sur différentes populations de patients."
    )

    # Métriques principales - Garder les 5 colonnes comme dans le code original
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("👥 Patients", len(df))
    col2.metric("Âge moyen", f"{df['age'].mean():.1f} ans")
    col3.metric("% Crohn", f"{(df['maladie'].str.contains('Crohn')).mean()*100:.1f}%")
    col4.metric("% RCH", f"{(df['maladie'].str.contains('RCH')).mean()*100:.1f}%")
    col5.metric("% MICI indét.", f"{(df['maladie']=='MICI indéterminée').mean()*100:.1f}%")

    # Répartition démographique
    st.subheader("📊 Caractéristiques des patients")
    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition par sexe avec Plotly
        fig_sexe = px.pie(
            df, 
            names="sexe",
            hole=0.3,
            title="Répartition par sexe"
        )
        st.plotly_chart(fig_sexe, use_container_width=True)
    
    with col2:
        # Distribution des âges avec Plotly
        fig_age = px.histogram(
            df,
            x="age",
            nbins=20,
            title="Distribution des âges"
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    # Répartition des maladies avec Plotly
    st.subheader("🦠 Types de MICI")
    freq_maladie = df["maladie"].value_counts().reset_index()
    fig_maladies = px.bar(
        freq_maladie,
        x="maladie",
        y="count",
        color="maladie",
        title="Répartition des maladies",
        labels={"maladie": "Type de MICI", "count": "Nombre de patients"}
    )
    st.plotly_chart(fig_maladies, use_container_width=True)

    # Top traitements avec Plotly
    st.subheader("💊 Top 5 des traitements")
    top_traitements = df["traitement"].value_counts().head(5).reset_index()
    fig_traitements = px.bar(
        top_traitements,
        x="count",
        y="traitement",
        orientation="h",
        text="count",
        title="Traitements les plus prescrits",
        labels={"traitement": "Traitement", "count": "Nombre de patients"}
    )
    fig_traitements.update_traces(textposition="outside")
    st.plotly_chart(fig_traitements, use_container_width=True)
    
    st.subheader("📱 Navigation")
    st.info(
        """
        Utilisez le menu de gauche pour explorer les différentes fonctionnalités :
        * **💊 Traitements** : Analyse détaillée de chaque traitement
        * **📊 Analyse comparative** : Comparaison des traitements entre eux
        """
    )

elif selected_page == "💊 Traitements":
    traitements(df)
elif selected_page == "📊 Analyse comparative":
    analyse_traitements(df)
elif selected_page == "⚠️ Pharmacovigilance":
    pharmacovigilance(df)
elif selected_page == "🔍 Recherche patients":
    recherche_patients(df)
elif selected_page == "🧠 Aide à la décision":
    aide_decision(df)
elif selected_page == "🔍 Extraction NLP":
    extraction_nlp(df)