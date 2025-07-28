# MediNLP

**MediNLP** est une application Streamlit de démonstration pour l’extraction d’informations médicales à partir de comptes-rendus en texte libre, avec un focus sur les maladies inflammatoires chroniques de l’intestin (MICI).

🌐 **Démo en ligne** : [https://medi-mici-nlp.streamlit.app/](https://medi-mici-nlp.streamlit.app/)

---

## Présentation

Ce projet propose une interface simple permettant :
- D’analyser un texte médical (compte-rendu, synthèse, etc.)
- D’extraire automatiquement les maladies, traitements et symptômes mentionnés
- De visualiser ces entités dans le texte (surlignage)
- D’obtenir un résumé automatique et une estimation de la sévérité
- D’explorer des relations entre traitements et symptômes (heatmap interactive)
- D’identifier des patients similaires dans une base fictive
- De générer un formulaire pré-rempli pour la structuration des données

L’approche est volontairement simple (mots-clés, expressions régulières) pour rester accessible et pédagogique.

---

## Inspiration

Ce projet s’inspire des besoins réels rencontrés dans la recherche clinique et l’épidémiologie, notamment autour des MICI.  
Il a été pensé à partir d’exemples publics et de problématiques rencontrées dans des projets hospitaliers (comme ceux de l’AP-HP), mais il n’est rattaché à aucun établissement et peut être adapté à d’autres contextes médicaux.

---

## User flow / Parcours utilisateur

1. **Accueil**  
   Vue d’ensemble de la base de données, statistiques globales et navigation.

2. **💊 Traitements**  
   Visualisation détaillée des traitements disponibles, leur fréquence et leur efficacité.

3. **📊 Analyse comparative**  
   Comparez l’efficacité, la tolérance et la répartition des traitements selon différents sous-groupes de patients (âge, sexe, maladie…).

4. **⚠️ Pharmacovigilance**  
   Analyse des effets secondaires rapportés pour chaque traitement et identification des profils à risque.

5. **🔍 Recherche patients**  
   Outil de recherche avancée pour filtrer et explorer les patients selon de multiples critères (âge, sexe, maladie, traitement, réponse…).

6. **🧠 Aide à la décision**  
   Simule une recommandation de traitement basée sur les profils similaires dans la base.

7. **🔍 Extraction NLP**  
   Permet d’analyser un texte médical libre, d’en extraire les entités (maladies, traitements, symptômes), de surligner ces entités dans le texte, d’obtenir un résumé automatique, une estimation de la sévérité, et de retrouver des patients similaires.

---

## Utilisation

- Rendez-vous sur [l’application Streamlit](https://medi-mici-nlp.streamlit.app/)
- Collez ou saisissez un texte médical dans la zone prévue (onglet Extraction NLP)
- Cliquez sur **Analyser le texte**
- Explorez les résultats, le surlignage, la heatmap et les autres fonctionnalités
- Naviguez dans les autres onglets pour explorer la base, comparer les traitements, etc.

---

## Fonctionnalités principales

- **Extraction d’entités médicales** (maladies, traitements, symptômes)
- **Surlignage dynamique** dans le texte
- **Résumé automatique** et score de sévérité
- **Heatmap interactive** (relations traitements/symptômes)
- **Recherche de patients similaires** (base fictive)
- **Formulaire structuré** pour la base de données
- **Analyse comparative, pharmacovigilance, aide à la décision**

---

## Limites & pistes d’amélioration

- Extraction basée sur des listes de mots-clés (pas de deep learning)
- Pas de gestion avancée des négations ou des contextes complexes
- Peut être adapté à d’autres pathologies ou contextes médicaux

---

## Licence

Projet open source, librement réutilisable et modifiable pour tout usage pédagogique, personnel ou professionnel.

---

## Auteur

Développé par Nabil  
Contact : nabil.erra5@gmail.com

---