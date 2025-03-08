import streamlit as st
import pandas as pd
from src.black_scholes import BlackScholesPricer

# Configuration de la page
st.set_page_config(page_title="Black-Scholes Pricer", page_icon="📈", layout="centered")

# Titre principal
st.title("📈 Pricer d'options Black-Scholes")

# Barre latérale pour les inputs
st.sidebar.header("📊 Paramètres de l'option")

S = st.sidebar.number_input("Prix du sous-jacent (S)", min_value=1.0, value=100.0, step=1.0)
K = st.sidebar.number_input("Prix d'exercice (K)", min_value=1.0, value=100.0, step=1.0)
T = st.sidebar.number_input("Temps à l'échéance (en années)", min_value=0.01, value=1.0, step=0.01)
r = st.sidebar.number_input("Taux sans risque (r, en %)", min_value=0.0, value=5.0, step=0.1) / 100
sigma = st.sidebar.number_input("Volatilité (σ, en %)", min_value=1.0, value=20.0, step=0.1) / 100

# Création du pricer
pricer = BlackScholesPricer(S, K, T, r, sigma)

# Calcul des prix des options
call_price = pricer.call_price()
put_price = pricer.put_price()

# Affichage du résumé des inputs sous forme de DataFrame sans index
st.subheader("📌 Résumé des paramètres")
df_params = pd.DataFrame({
    "Paramètre": ["Prix du sous-jacent (S)", "Prix d'exercice (K)", "Temps à l'échéance (T)", "Taux sans risque (r)", "Volatilité (σ)"],
    "Valeur": [f"{S}€",f"{K}€", f"{T} ans", f"{r*100:.2f}%", f"{sigma*100:.2f}%"]
})
st.table(df_params.set_index("Paramètre"))  # Suppression de l'index par défaut


# Affichage des résultats sous forme de cartes
st.subheader("📌 Prix des options")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style="padding:20px; border-radius:10px; background-color:#1E88E5; color:white; text-align:center;">
            <h2>💰 Call</h2>
            <h1>{call_price:.2f} €</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="padding:20px; border-radius:10px; background-color:#D81B60; color:white; text-align:center;">
            <h2>💰 Put</h2>
            <h1>{put_price:.2f} €</h1>
        </div>
        """,
        unsafe_allow_html=True
    )


