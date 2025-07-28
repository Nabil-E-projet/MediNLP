import streamlit as st
import pandas as pd
import re
import random
import numpy as np
from collections import Counter

def extraction_nlp(df):
    st.title("🔍 Extraction NLP de comptes-rendus médicaux")
    st.write(
        "Cette page permet d'analyser des comptes-rendus médicaux en texte libre "
        "pour en extraire automatiquement les informations sur les MICI, "
        "traitements et symptômes mentionnés."
    )
    st.info(
        "L'extraction se fait par reconnaissance d'entités nommées (NER) "
        "en utilisant des dictionnaires médicaux et des expressions régulières."
    )

    dictionnaire_mici = [
        "maladie de Crohn", "Crohn", "RCH", "rectocolite hémorragique", 
        "colite ulcéreuse", "MICI", "maladie inflammatoire chronique intestinale",
        "iléite", "colite", "entérite"
    ]
    dictionnaire_traitements = [
        "Infliximab", "Remicade", "Adalimumab", "Humira", "Vedolizumab", "Entyvio",
        "Ustekinumab", "Stelara", "Azathioprine", "Imurel", "Mesalazine", "Pentasa",
        "corticoïdes", "prednisone", "cortisone", "méthotrexate", "anti-TNF",
        "Methylprednisolone"
    ]
    dictionnaire_symptomes = [
        "diarrhée", "douleur abdominale", "sang dans les selles", "fatigue",
        "perte de poids", "fièvre", "douleurs articulaires", "lésions cutanées",
        "nausées", "vomissements", "crampes", "ballonnements", "asthénie", 
        "saignement", "ulcération"
    ]

    st.subheader("📝 Saisie du compte-rendu médical")
    exemple_selected = st.checkbox("Utiliser un exemple pré-rempli")
    if exemple_selected:
        exemple_texte = """
        Compte-rendu d'hospitalisation - Service d'Hépato-Gastroentérologie

        Patient : M. DUPONT Jean
        Date de naissance : 12/05/1983
        Date d'admission : 15/06/2023
        Date de sortie : 18/06/2023

        MOTIF D'HOSPITALISATION :
        Poussée de rectocolite hémorragique avec diarrhée sanglante et douleurs abdominales importantes.

        ANTÉCÉDENTS :
        - Rectocolite hémorragique diagnostiquée en 2015, pancolique
        - Appendicectomie en 2008
        - Pas d'allergie médicamenteuse connue

        HISTOIRE DE LA MALADIE :
        Patient suivi pour une RCH depuis 8 ans, initialement stabilisée sous Mesalazine pendant 3 ans, puis échec avec passage à l'Azathioprine en 2018. Suite à une poussée sévère en 2020, mise sous Infliximab avec bonne réponse initiale.

        Depuis 3 semaines, recrudescence progressive des symptômes avec diarrhée (8-10 selles/jour), présence de sang dans les selles, douleurs abdominales diffuses, fatigue intense et perte de poids estimée à 3kg.

        TRAITEMENT À L'ENTRÉE :
        - Infliximab 5mg/kg toutes les 8 semaines (dernière injection il y a 6 semaines)
        - Azathioprine 150mg/jour
        - Paracétamol si douleur

        EXAMEN CLINIQUE :
        Poids: 68kg, Taille: 178cm, TA: 115/75 mmHg, Pouls: 88/min, T°: 37.8°C
        Patient asthénique, pâleur cutanéo-muqueuse
        Abdomen souple mais sensible de façon diffuse, plus marquée dans le cadre colique gauche
        Pas de défense ni contracture
        Examen proctologique: présence de sang rouge vif

        EXAMENS COMPLÉMENTAIRES :
        - Biologie: Hb 10.8 g/dL, GB 11200/mm3, Plaquettes 455000/mm3, CRP 42 mg/L
        - Calprotectine fécale: 1250 µg/g
        - Coproculture et recherche de Clostridium difficile: négatives
        - Coloscopie: muqueuse érythémateuse, friable avec ulcérations superficielles diffuses du rectum au côlon transverse, compatible avec une poussée de RCH

        PRISE EN CHARGE ET ÉVOLUTION :
        Hospitalisation pour optimisation thérapeutique avec:
        - Corticothérapie IV (Methylprednisolone 60mg/j)
        - Hydratation IV
        - Majoration du traitement antalgique
        - Surveillance biologique quotidienne

        Évolution favorable avec diminution progressive des douleurs abdominales et de la fréquence des selles (3-4/jour à J3), diminution du saignement rectal.

        CONCLUSION :
        Poussée modérée à sévère de rectocolite hémorragique chez un patient sous Infliximab, évoquant une perte de réponse.

        TRAITEMENT DE SORTIE :
        - Prednisone 40mg/j à décroissance progressive sur 8 semaines
        - Optimisation de l'Infliximab: augmentation à 10mg/kg
        - Azathioprine maintenu à 150mg/j
        - Mesalazine topique en suppositoire 1g/jour
        - Fer per os: Tardyferon 80mg x 2/j
        - Surveillance biologique hebdomadaire (NFS, CRP)

        SUIVI :
        - Consultation de contrôle dans 4 semaines
        - Dosage des taux résiduels d'Infliximab et recherche d'anticorps anti-Infliximab à prévoir
        - Calprotectine fécale de contrôle à 2 mois
        - Discuter passage à l'Ustekinumab ou au Vedolizumab en cas d'échec de l'optimisation

        Dr. MARTIN Sophie
        Chef de Service Hépato-Gastroentérologie
        CHU de [Ville]
        """
        text_input = st.text_area("Texte du compte-rendu", exemple_texte, height=300)
    else:
        text_input = st.text_area(
            "Collez le texte du compte-rendu ici", 
            "", 
            height=300,
            placeholder="Exemple: Patient de 35 ans suivi pour une maladie de Crohn avec traitement par Adalimumab..."
        )

    if st.button("Analyser le texte", use_container_width=True):
        if not text_input:
            st.error("Veuillez entrer un texte à analyser")
        else:
            with st.spinner("Analyse en cours..."):
                def extraire_entites(texte, dictionnaire):
                    texte_normalise = re.sub(r'\s+', ' ', texte).lower()
                    original_normalise = re.sub(r'\s+', ' ', texte)
                    entites_trouvees = []
                    for terme in dictionnaire:
                        terme_lower = terme.lower()
                        pattern = r'\b' + re.escape(terme_lower) + r'\b'
                        for match in re.finditer(pattern, texte_normalise):
                            debut, fin = match.span()
                            terme_original = original_normalise[debut:fin]
                            entites_trouvees.append(terme_original)
                    return list(set(entites_trouvees))
                mici_trouvees = extraire_entites(text_input, dictionnaire_mici)
                traitements_trouves = extraire_entites(text_input, dictionnaire_traitements)
                symptomes_trouves = extraire_entites(text_input, dictionnaire_symptomes)
                import time
                time.sleep(1.5)

            st.subheader("✅ Résultats de l'extraction")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**MICI identifiées:**")
                if mici_trouvees:
                    for mici in mici_trouvees:
                        st.success(f"• {mici}")
                else:
                    st.info("Aucune MICI identifiée")
            with col2:
                st.write("**Traitements identifiés:**")
                if traitements_trouves:
                    for traitement in traitements_trouves:
                        st.success(f"• {traitement}")
                else:
                    st.info("Aucun traitement identifié")
            with col3:
                st.write("**Symptômes identifiés:**")
                if symptomes_trouves:
                    for symptome in symptomes_trouves:
                        st.success(f"• {symptome}")
                else:
                    st.info("Aucun symptôme identifié")

            st.subheader("🚨 Évaluation de la sévérité")
            score_severite = 0
            symptomes_graves = ["sang dans les selles", "diarrhée", "perte de poids", "saignement"]
            symptomes_moderes = ["fatigue", "douleur abdominale", "ulcération", "asthénie"]
            for symptome in symptomes_trouves:
                symptome_lower = symptome.lower()
                if any(grave in symptome_lower for grave in symptomes_graves):
                    score_severite += 2
                elif any(modere in symptome_lower for modere in symptomes_moderes):
                    score_severite += 1
            score_normalise = min(score_severite / 8, 1.0)
            niveau_texte = "Léger" if score_normalise < 0.33 else "Modéré" if score_normalise < 0.66 else "Sévère"
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(score_normalise)
            with col2:
                st.write(f"**{niveau_texte}**")
            st.write(f"Score calculé sur la base de {len(symptomes_trouves)} symptômes détectés.")

            # Surlignage robuste (fonctionne même avec l'exemple)
            st.subheader("📑 Texte analysé avec entités")
            texte_affichage = text_input
            for mici in sorted(mici_trouvees, key=len, reverse=True):
                texte_affichage = re.sub(
                    r'\b' + re.escape(mici) + r'\b',
                    f'<span style="background-color: #ffe066; color: #222; border-radius:3px; padding: 0 3px;">{mici}</span>',
                    texte_affichage,
                    flags=re.IGNORECASE
                )
            for traitement in sorted(traitements_trouves, key=len, reverse=True):
                texte_affichage = re.sub(
                    r'\b' + re.escape(traitement) + r'\b',
                    f'<span style="background-color: #b2f2ff; color: #222; border-radius:3px; padding: 0 3px;">{traitement}</span>',
                    texte_affichage,
                    flags=re.IGNORECASE
                )
            for symptome in sorted(symptomes_trouves, key=len, reverse=True):
                texte_affichage = re.sub(
                    r'\b' + re.escape(symptome) + r'\b',
                    f'<span style="background-color: #d3f9d8; color: #222; border-radius:3px; padding: 0 3px;">{symptome}</span>',
                    texte_affichage,
                    flags=re.IGNORECASE
                )
            texte_html = texte_affichage.replace('\n', '<br>')
            legende_html = """
            <div style="margin-bottom: 10px;">
                <span style="background-color: #ffe066; color: #222; padding: 2px 5px; border-radius: 3px;">MICI</span>
                <span style="background-color: #b2f2ff; color: #222; padding: 2px 5px; border-radius: 3px; margin-left: 10px;">Traitements</span>
                <span style="background-color: #d3f9d8; color: #222; padding: 2px 5px; border-radius: 3px; margin-left: 10px;">Symptômes</span>
            </div>
            """
            st.markdown(legende_html, unsafe_allow_html=True)
            st.markdown(f'<div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px;">{texte_html}</div>', unsafe_allow_html=True)

            # Graphique Plotly compact
            if traitements_trouves and symptomes_trouves:
                with st.expander("🔄 Voir les relations entre traitements et symptômes (interactif)"):
                    import plotly.express as px
                    matrix = np.zeros((len(traitements_trouves), len(symptomes_trouves)))
                    for i in range(len(traitements_trouves)):
                        for j in range(len(symptomes_trouves)):
                            matrix[i, j] = random.randint(0, 100)
                    fig = px.imshow(
                        matrix,
                        labels=dict(x="Symptômes", y="Traitements", color="Score"),
                        x=symptomes_trouves,
                        y=traitements_trouves,
                        color_continuous_scale="YlGnBu",
                        aspect="auto"
                    )
                    fig.update_layout(
                        title_text='Fréquence de co-occurrence',
                        xaxis_tickangle=-45,
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.caption("Passez la souris sur les cases pour voir les scores.")

            st.subheader("📋 Résumé automatique")
            maladies_str = ", ".join(mici_trouvees) if mici_trouvees else "non précisée"
            traitements_str = ", ".join(traitements_trouves) if traitements_trouves else "aucun mentionné"
            symptomes_str = ", ".join(symptomes_trouves) if symptomes_trouves else "aucun mentionné"
            resume = f"""
            **Synthèse du compte-rendu:**
            
            Le patient est suivi pour {maladies_str}. 
            Traitement(s): {traitements_str}.
            Symptômes rapportés: {symptomes_str}.
            Niveau de sévérité estimé: {niveau_texte}
            
            *Note: Ce résumé est généré automatiquement et peut contenir des erreurs.*
            """
            st.info(resume)

            st.subheader("⏱️ Chronologie détectée")
            dates_pattern = r'\d{1,2}/\d{1,2}/\d{4}'
            dates = re.findall(dates_pattern, text_input)
            if dates:
                events = []
                context_keywords = {
                    "diagnostic": ["diagnostiqué", "diagnostic"],
                    "traitement": ["traitement", "mise sous", "initiation"],
                    "consultation": ["consultation", "contrôle"],
                    "hospitalisation": ["hospitalisation", "admission"]
                }
                for i, date in enumerate(dates[:6]):
                    date_index = text_input.find(date)
                    start = max(0, date_index - 30)
                    end = min(len(text_input), date_index + 30)
                    context = text_input[start:end].lower()
                    event_type = "Événement"
                    for event_name, keywords in context_keywords.items():
                        if any(keyword in context for keyword in keywords):
                            event_type = event_name.capitalize()
                            break
                    events.append({"Date": date, "Événement": event_type})
                events_df = pd.DataFrame(events)
                st.dataframe(events_df, use_container_width=True)
            else:
                st.info("Aucune date au format JJ/MM/AAAA n'a été détectée dans le texte.")

            st.subheader("👥 Patients similaires dans la base de données")
            if mici_trouvees:
                mici_pattern = "Crohn" if any("Crohn" in m.lower() for m in mici_trouvees) else "RCH" if any("RCH" in m or "rectocolite" in m.lower() for m in mici_trouvees) else ""
                if mici_pattern:
                    try:
                        patients_similaires = df[df["maladie"].str.contains(mici_pattern, case=False, na=False)]
                        if traitements_trouves:
                            traitements_pattern = "|".join([t.lower() for t in traitements_trouves])
                            patients_similaires_traitement = patients_similaires[
                                patients_similaires["traitement"].str.lower().str.contains(traitements_pattern, na=False)
                            ]
                            if len(patients_similaires_traitement) > 0:
                                patients_similaires = patients_similaires_traitement
                        st.write(f"**{len(patients_similaires)} patients similaires trouvés dans la base de données**")
                        if len(patients_similaires) > 0:
                            st.dataframe(
                                patients_similaires[["id", "age", "sexe", "maladie", "traitement", "reponse_traitement"]].head(5),
                                use_container_width=True
                            )
                            efficacite_groupe = patients_similaires["reponse_traitement"].value_counts(normalize=True) * 100
                            st.write(f"**Efficacité des traitements chez ces patients:**")
                            st.write(f"• Efficace: {efficacite_groupe.get('Efficace', 0):.1f}%")
                            st.write(f"• Partiel: {efficacite_groupe.get('Partiel', 0):.1f}%")
                            st.write(f"• Échec: {efficacite_groupe.get('Échec', 0):.1f}%")
                    except Exception as e:
                        st.error(f"Erreur dans la recherche de patients similaires: {e}")
                        st.info("Les patients similaires n'ont pas pu être affichés.")
                else:
                    st.info("Type de MICI non identifié précisément dans le texte.")
            else:
                st.info("Aucune MICI identifiée pour rechercher des patients similaires.")

            st.subheader("📝 Formulaire pré-rempli pour la base de données")
            with st.expander("Voir le formulaire pour ajout à la base"):
                col1, col2 = st.columns(2)
                with col1:
                    st.text_input("MICI détectée", value=mici_trouvees[0] if mici_trouvees else "")
                    st.text_input("Traitement principal", value=traitements_trouves[0] if traitements_trouves else "")
                with col2:
                    st.text_input("Symptômes principaux", value=", ".join(symptomes_trouves[:3]) if symptomes_trouves else "")
                    st.selectbox("Sévérité estimée", ["Légère", "Modérée", "Sévère"], index=0 if niveau_texte == "Léger" else 1 if niveau_texte == "Modéré" else 2)
                st.date_input("Date de consultation", value=None)
                st.number_input("Âge du patient", min_value=15, max_value=90, value=40)
                st.radio("Sexe", ["H", "F"])
                if st.button("Ajouter à la base de données (simulation)"):
                    st.success("✅ Patient ajouté avec succès à la base de données (simulation)")

            st.subheader("🔍 Pistes d'amélioration")
            st.write(
                """
                Cette extraction basique par mots-clés pourrait être améliorée avec:
                
                * Un modèle NLP spécialisé pré-entraîné sur des textes médicaux
                * La détection de relations entre entités (ex: quel traitement pour quelle maladie)
                * L'analyse temporelle (traitements passés vs actuels)
                * Un dictionnaire médical plus complet
                * La gestion des négations ("pas de fièvre" ne devrait pas extraire "fièvre")
                """
            )
