
import streamlit as st
import json
import os
import base64
from datetime import date

st.set_page_config(page_title="AVAX", page_icon="🌌", layout="centered")

FICHIER = "utilisateurs.json"
LIEN_DISCORD = "https://discord.gg/8m7KwCyjW"
MOT_DE_PASSE_ADMIN = "Admin123"

# DESIGN
st.markdown("""
<style>
.stApp {
    background-color: #080810;
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.stTextInput input, .stDateInput input {
    background-color: #171722 !important;
    color: white !important;
    border: 1px solid #8b5cf6 !important;
}
.stButton button, .stFormSubmitButton button {
    background-color: #7135d9 !important;
    color: white !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)


# FONCTIONS
def charger_utilisateurs():
    if os.path.exists(FICHIER):
        with open(FICHIER, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def sauvegarder_utilisateurs(utilisateurs):
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(utilisateurs, f, ensure_ascii=False, indent=4)


# ADMINISTRATION CACHEE
if st.query_params.get("page") == "admin":

    st.title("🔐 Administration AVAX")

    if not st.session_state.get("admin_connecte", False):

        mdp = st.text_input("Mot de passe", type="password")

        if st.button("Se connecter"):
            if mdp == MOT_DE_PASSE_ADMIN:
                st.session_state.admin_connecte = True
                st.rerun()
            else:
                st.error("Mot de passe incorrect.")

    else:
        utilisateurs = charger_utilisateurs()

        st.success("Bienvenue administrateur !")
        st.metric("Nombre d'inscriptions", len(utilisateurs))

        if utilisateurs:
            st.dataframe(utilisateurs, use_container_width=True)
        else:
            st.info("Aucune inscription.")

        if st.button("Déconnexion"):
            st.session_state.admin_connecte = False
            st.rerun()


# PAGE VISITEURS
else:

    if st.session_state.get("inscription_terminee", False):

        st.title("🎉 Bienvenue chez AVAX !")
        st.write("Ton inscription est terminée.")

        st.link_button(
            "🚀 REJOINDRE LE SERVEUR DISCORD",
            LIEN_DISCORD,
            use_container_width=True
        )

        # ANIMATION GIF
        st.write(" ")
        if os.path.exists("rejoindre.gif"):
            with open("rejoindre.gif", "rb") as f:
                gif = base64.b64encode(f.read()).decode()

            st.markdown(
                f'<img src="data:image/gif;base64,{gif}" width="100%">',
                unsafe_allow_html=True
            )
        else:
            st.warning("Le fichier rejoindre.gif est introuvable.")

    else:

        st.title("🌌 AVAX")
        st.subheader("Inscription au serveur Discord")
        st.write("Remplis les informations pour continuer.")

        with st.form("inscription"):

            prenom = st.text_input("Prénom")
            nom = st.text_input("Nom")

            naissance = st.date_input(
                "Date de naissance",
                value=date(2000, 1, 1),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                format="DD/MM/YYYY"
            )

            confirmation = st.checkbox(
                "J'accepte que mes informations soient enregistrées."
            )

            envoyer = st.form_submit_button("Valider")

            if envoyer:
                if not prenom.strip() or not nom.strip():
                    st.warning("Remplis ton prénom et ton nom.")

                elif not confirmation:
                    st.warning("Coche la case de confirmation.")

                else:
                    utilisateurs = charger_utilisateurs()

                    utilisateurs.append({
                        "Prénom": prenom.strip(),
                        "Nom": nom.strip(),
                        "Date de naissance": naissance.strftime("%d/%m/%Y"),
                        "Date d'inscription": date.today().strftime("%d/%m/%Y")
                    })

                    sauvegarder_utilisateurs(utilisateurs)

                    st.session_state.inscription_terminee = True
                    st.rerun()
