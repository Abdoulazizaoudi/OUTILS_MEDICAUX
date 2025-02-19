import streamlit as st

# Configuration initiale
if "page" not in st.session_state:
    st.session_state.page = "accueil"

if "user_count" not in st.session_state:
    st.session_state.user_count = 0
st.session_state.user_count += 1


# =============================================
# FONCTIONS COMMUNES
# =============================================

def navigation():
    if st.button("← Retour à l'accueil"):
        st.session_state.page = "accueil"


# =============================================
# PAGE ACCUEIL
# =============================================

def accueil():
    st.title("🩺 OUTILS MEDICAUX")
    st.caption(f"Utilisateurs connectés : {st.session_state.user_count}")
    st.header("Sélectionnez un calculateur", divider="rainbow")

    with st.container():
        st.subheader("1. Indice de Masse Corporelle (IMC)")
        st.write("Classification OMS - Évaluation du statut pondéral")
        if st.button("Accéder → IMC", key="imc_btn"):
            st.session_state.page = "imc"
        st.markdown("---")

    with st.container():
        st.subheader("2. Clairance de la Créatinine")
        st.write("Formule Cockcroft-Gault - Fonction rénale")
        if st.button("Accéder → Clairance", key="crea_btn"):
            st.session_state.page = "creatinine"
        st.markdown("---")


# =============================================
# CALCULATEUR IMC
# =============================================

def page_imc():
    st.title("📏 Calculateur d'IMC")

    with st.form(key="form_imc"):
        col1, col2 = st.columns(2)
        with col1:
            poids = st.number_input("Poids (kg)",
                                    min_value=30.0,
                                    max_value=300.0,
                                    value=70.0,
                                    step=0.1)
        with col2:
            taille = st.number_input("Taille (m)",
                                     min_value=1.0,
                                     max_value=2.5,
                                     value=1.75,
                                     step=0.01,
                                     format="%.2f")

        if st.form_submit_button("Calculer l'IMC"):
            if taille > 0:
                imc = poids / (taille ** 2)
                healthy_min = 18.5 * (taille ** 2)
                healthy_max = 24.9 * (taille ** 2)

                # Affichage résultats
                st.subheader("Résultats", divider="green")
                st.metric("Votre IMC", f"{imc:.2f} kg/m²")

                # Interprétation
                if imc < 18.5:
                    diff = healthy_min - poids
                    st.error("INSUFFISANCE PONDÉRALE")
                    st.markdown(f"""
                    **Objectif santé :**  
                    → Gain de poids recommandé : **{diff:.1f} kg**  
                    - Poids minimal conseillé : **{healthy_min:.1f} kg**
                    """)

                elif 18.5 <= imc < 25:
                    st.success("POIDS NORMAL")
                    st.markdown(f"""
                    **Plage de poids sain :**  
                    - Minimum : **{healthy_min:.1f} kg**  
                    - Maximum : **{healthy_max:.1f} kg**
                    """)

                elif 25 <= imc < 30:
                    diff = poids - healthy_max
                    st.warning("SURPOIDS")
                    st.markdown(f"""
                    **Objectif santé :**  
                    → Perte de poids recommandée : **{diff:.1f} kg**  
                    - Poids maximal conseillé : **{healthy_max:.1f} kg**
                    """)

                else:
                    diff = poids - healthy_max
                    if imc < 35:
                        classe = "Classe I (Obésité modérée)"
                    elif imc < 40:
                        classe = "Classe II (Obésité sévère)"
                    else:
                        classe = "Classe III (Obésité morbide)"

                    st.error(f"OBÉSITÉ ({classe})")
                    st.markdown(f"""
                    **Action nécessaire :**  
                    → Perte de poids minimale : **{diff:.1f} kg**  
                    - Premier objectif : **{healthy_max:.1f} kg**
                    """)

                # Référence
                st.markdown("---")
                st.markdown("""
                **Classification OMS :**  
                [Surpoids et obésité - OMS](https://www.who.int/fr/news-room/fact-sheets/detail/obesity-and-overweight)  
                *Mise à jour 2024 - Organisation Mondiale de la Santé*
                """)

            else:
                st.error("La taille doit être supérieure à 0 !")

    navigation()


# =============================================
# CALCULATEUR CLAIRANCE
# =============================================

def calcul_clairance(age, sexe, poids, creatinine):
    return ((140 - age) * poids * (0.85 if sexe == "Femme" else 1)) / (72 * creatinine)


def page_creatinine():
    st.title("🧪 Clairance de la Créatinine")

    with st.form(key="form_creatinine"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Âge (années)",
                                  min_value=18,
                                  max_value=120,
                                  value=50)
            sexe = st.radio("Sexe", ["Homme", "Femme"])
        with col2:
            poids = st.number_input("Poids (kg)",
                                    min_value=40.0,
                                    max_value=200.0,
                                    value=70.0)
            creatinine = st.number_input("Créatinine (mg/dL)",
                                         min_value=0.1,
                                         max_value=10.0,
                                         value=1.0,
                                         step=0.1)

        if st.form_submit_button("Calculer"):
            resultat = calcul_clairance(age, sexe, poids, creatinine)

            st.subheader("Résultats", divider="blue")
            st.metric("Clairance estimée", f"{resultat:.2f} mL/min")

            # Interprétation
            if resultat >= 90:
                st.success("Fonction rénale normale")
            elif 60 <= resultat < 90:
                st.warning("Insuffisance rénale légère (Stade 2)")
            elif 30 <= resultat < 60:
                st.error("Insuffisance rénale modérée (Stade 3)")
            elif 15 <= resultat < 30:
                st.error("Insuffisance rénale sévère (Stade 4)")
            else:
                st.error("Insuffisance rénale terminale (Stade 5)")

            # Recommandations
            st.markdown("---")
            st.subheader("Conduite à tenir")
            if resultat >= 60:
                st.markdown("""
                - Surveillance annuelle
                - Éviter les néphrotoxiques
                - Hydratation suffisante
                """)
            elif 30 <= resultat < 60:
                st.markdown("""
                - Consultation néphrologique
                - Adaptation posologies
                - Bilan étiologique
                """)
            else:
                st.markdown("""
                - Prise en charge urgente
                - Préparation dialyse
                - Suivi spécialisé
                """)

    # Références
    st.markdown("---")
    st.markdown("""
    **Références scientifiques :**  
    1. Cockcroft DW, Gault MH. Prediction of creatinine clearance from serum creatinine. *Nephron*. 1976  
    2. KDIGO 2023 Clinical Practice Guideline for CKD Evaluation  
    3. HAS - Prise en charge de l'insuffisance rénale chronique (2024)
    """)

    navigation()


# =============================================
# GESTION DES PAGES
# =============================================

if st.session_state.page == "accueil":
    accueil()
elif st.session_state.page == "imc":
    page_imc()
elif st.session_state.page == "creatinine":
    page_creatinine()

# =============================================
# PIED DE PAGE
# =============================================

st.markdown("---")
st.caption("""
Développé par Dr. Abdoulaziz Aoudi  
Data Scientist  | © 2025 - Tous droits réservés  
""")