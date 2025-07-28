import streamlit as st
import pandas as pd
import plotly.express as px

def traitements(df):
    # 1 Titre et description
    st.title("💊 Analyse des traitements")
    st.write("Explore l'efficacité des traitements et leur évolution dans la cohorte.")

    #  Sélection du traitement
    traitements_disponibles = sorted(df["traitement"].unique())
    selected = st.selectbox("Sélectionner un traitement :", traitements_disponibles)

    #  Filtrer les données pour le traitement choisi
    df_sel = df[df["traitement"] == selected]

    #  KPIs clés
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Patients", len(df_sel))
    col2.metric("% de la cohorte", f"{len(df_sel)/len(df)*100:.1f}%")
    col3.metric("🎯 Efficacité", f"{(df_sel['reponse_traitement'] == 'Efficace').mean()*100:.1f}%" )
    # Pie et graphique temporel côte à côte
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"📊 Efficacité - {selected}")
        status_counts = (
            df_sel["reponse_traitement"]
            .value_counts()
            .rename_axis("statut")
            .reset_index(name="count")
        )
        fig1 = px.pie(
            status_counts,
            values="count",
            names="statut",
            title="Répartition des statuts cliniques"
        )
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.subheader("📈 Évolution temporelle")
        if "date_consultation" in df_sel.columns:
            # Regroupement par trimestre pour lisser le graphique
            df_time = (
                pd.to_datetime(df_sel["date_consultation"], format="%d-%m-%Y", errors="coerce")
                .dt.to_period("Q")  # "Q" pour trimestre
                .value_counts()
                .sort_index()
                .rename_axis("trimestre")
                .reset_index(name="count")
            )
            df_time["trimestre"] = df_time["trimestre"].dt.to_timestamp()
        else:
            # Simulation sur 12 trimestres
            dates = pd.date_range("2023-01-01", periods=12, freq="Q")
            counts = [len(df_sel) * (i+1) // 12 for i in range(12)]
            df_time = pd.DataFrame({"trimestre": dates, "count": counts})

        fig2 = px.line(
            df_time,
            x="trimestre",
            y="count",
            title="Évolution du nombre de patients (par trimestre)"
        )
        st.plotly_chart(fig2, use_container_width=True)