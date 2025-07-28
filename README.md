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

## Utilisation

- Rendez-vous sur [l’application Streamlit](https://medi-mici-nlp.streamlit.app/)
- Collez ou saisissez un texte médical dans la zone prévue
- Cliquez sur **Analyser le texte**
- Explorez les résultats, le surlignage, la heatmap et les autres fonctionnalités

---

## Fonctionnalités principales

- **Extraction d’entités médicales** (maladies, traitements, symptômes)
- **Surlignage dynamique** dans le texte
- **Résumé automatique** et score de sévérité
- **Heatmap interactive** (relations traitements/symptômes)
- **Recherche de patients similaires** (base fictive)
- **Formulaire structuré** pour la base de données

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

Contact : nabil.erra5@gmail.com

---