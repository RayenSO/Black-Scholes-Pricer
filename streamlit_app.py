import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.black_scholes import BlackScholesPricer
from src.market_data import get_last_price
from src.risk_free_rate import get_risk_free_rate


# Configuration de la page
st.set_page_config(page_title="Black-Scholes Pricer", page_icon="📈", layout="centered")

# Titre principal
st.title("📈 Pricer d'options Black-Scholes")

# Barre latérale pour les inputs
st.sidebar.header("📊 Paramètres de l'option")

# Saisie directe du ticker
ticker = st.sidebar.text_input("Entrez un ticker (ex: AAPL, TSLA, MSFT)")

S = None
if ticker:
    last_price = get_last_price(ticker.upper())  # Récupération du prix avec le ticker entré
    if last_price:
        st.sidebar.success(f"📊 Prix actuel : {last_price:.2f} €")
        S = last_price  # Stockage du prix récupéré
    else:
        st.sidebar.error("Impossible de récupérer le prix. Vérifiez le ticker.")

# Vérification avant d'instancier le pricer
if S is not None:
    K = st.sidebar.number_input("Prix d'exercice (K, en €)", min_value=1.0, value=100.0, step=1.0)

    # Sélection du type d'échéance
    echeance_type = st.sidebar.selectbox("Type d'échéance", ["Jours", "Mois", "Années"])

    # Entrée de la durée selon l'unité choisie
    echeance_valeur = st.sidebar.number_input(f"Durée ({echeance_type})", min_value=1, value=1, step=1)

    # Conversion en années pour le modèle
    if echeance_type == "Jours":
        T = echeance_valeur / 252
        echeance_affichage = f"{int(echeance_valeur)} jours"
    elif echeance_type == "Mois":
        T = echeance_valeur / 12
        echeance_affichage = f"{echeance_valeur} mois"
    else:  # "Années"
        T = echeance_valeur
        echeance_affichage = f"{echeance_valeur} ans"

    # Sélection de la méthode du taux sans risque
    r_choice = st.sidebar.radio("Choisir la source du taux sans risque :", ["US Treasury 10Y", "Entrée manuelle"])

    if r_choice == "US Treasury 10Y":
        r = get_risk_free_rate("US Treasury 10Y")
        if r is not None:
            st.sidebar.success(f"📌 Taux sans risque (10Y Treasury) : {r*100:.2f} %")
        else:
            r = st.sidebar.number_input("Taux sans risque (r, en %)", min_value=0.0, value=5.0, step=0.1) / 100
    else:
        r = st.sidebar.number_input("Taux sans risque (r, en %)", min_value=0.0, value=5.0, step=0.1) / 100
    sigma = st.sidebar.number_input("Volatilité (σ, en %)", min_value=0.0, value=20.0, step=0.1) / 100

    # Création du pricer
    pricer = BlackScholesPricer(S, K, T, r, sigma)

    # Calcul des prix des options
    call_price = pricer.call_price()
    put_price = pricer.put_price()

    # Affichage du résumé des inputs sous forme de DataFrame sans index
    st.subheader("📌 Résumé des paramètres")
    df_params = pd.DataFrame({
        "Paramètre": ["Prix du sous-jacent (S)", "Prix d'exercice (K)", "Temps à l'échéance", "Taux sans risque (r)", "Volatilité (σ)"],
        "Valeur": [f"{S:.2f} €", f"{K:.2f} €", echeance_affichage, f"{r*100:.2f}%", f"{sigma*100:.2f}%"]
    })
    st.table(df_params.set_index("Paramètre"))

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

    # Génération des valeurs de S pour les graphiques
    S_values = [S * (0.5 + i * 0.05) for i in range(20)]  # De 50% S à 150% S

    # Calcul des prix et Greeks pour chaque valeur de S
    call_prices, put_prices = [], []
    delta_values, gamma_values, vega_values, theta_values, rho_values = [], [], [], [], []

    for S_var in S_values:
        pricer_temp = BlackScholesPricer(S_var, K, T, r, sigma)
        call_prices.append(pricer_temp.call_price())
        put_prices.append(pricer_temp.put_price())
        delta_values.append(pricer_temp.delta("call"))
        gamma_values.append(pricer_temp.gamma())
        vega_values.append(pricer_temp.vega())
        theta_values.append(pricer_temp.theta("call"))
        rho_values.append(pricer_temp.rho("call"))

    # 📊 Graphique des Prix des Options 📊
    st.subheader("📊 Prix des Options en fonction du Sous-Jacent")

    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(x=S_values, y=call_prices, mode="lines", name="Call Price", line=dict(color="blue")))
    fig_price.add_trace(go.Scatter(x=S_values, y=put_prices, mode="lines", name="Put Price", line=dict(color="red")))

    fig_price.update_layout(
        xaxis_title="Prix du Sous-Jacent (S)",
        yaxis_title="Prix de l'Option (€)",
        legend=dict(x=0, y=1),
        template="plotly_white"
    )
    st.plotly_chart(fig_price, use_container_width=True)

    # Calcul des Greeks
    delta_call = pricer.delta("call")
    delta_put = pricer.delta("put")
    gamma = pricer.gamma()
    vega = pricer.vega()
    theta_call = pricer.theta("call")
    theta_put = pricer.theta("put")
    rho_call = pricer.rho("call")
    rho_put = pricer.rho("put")

    # Affichage des Greeks sous forme de tableau
    st.subheader("📊 Greeks des options")

    df_greeks = pd.DataFrame({
        "Greek": ["Delta", "Gamma", "Vega", "Theta", "Rho"],
        "Call": [f"{delta_call:.4f}", f"{gamma:.4f}", f"{vega:.4f}", f"{theta_call:.4f}", f"{rho_call:.4f}"],
        "Put": [f"{delta_put:.4f}", f"{gamma:.4f}", f"{vega:.4f}", f"{theta_put:.4f}", f"{rho_put:.4f}"]
    })

    st.table(df_greeks.set_index("Greek"))

    # 📈 Graphique des Greeks 📈
    st.subheader("📊 Greeks en fonction du Sous-Jacent")

    fig_greeks = go.Figure()
    fig_greeks.add_trace(go.Scatter(x=S_values, y=delta_values, mode="lines", name="Delta", line=dict(color="green")))
    fig_greeks.add_trace(go.Scatter(x=S_values, y=gamma_values, mode="lines", name="Gamma", line=dict(color="purple")))
    fig_greeks.add_trace(go.Scatter(x=S_values, y=vega_values, mode="lines", name="Vega", line=dict(color="orange")))
    fig_greeks.add_trace(go.Scatter(x=S_values, y=theta_values, mode="lines", name="Theta", line=dict(color="brown")))
    fig_greeks.add_trace(go.Scatter(x=S_values, y=rho_values, mode="lines", name="Rho", line=dict(color="pink")))

    fig_greeks.update_layout(
        xaxis_title="Prix du Sous-Jacent (S)",
        yaxis_title="Valeur des Greeks",
        legend=dict(x=0, y=1),
        template="plotly_white"
    )
    st.plotly_chart(fig_greeks, use_container_width=True)
else:
    st.warning("⏳ En attente de la sélection d'un actif et de la récupération du prix...")

# Pied de page
st.markdown("---")
st.caption("📌 Développé avec ❤️ par Rayen & Eliasy | Modèle Black-Scholes pour le pricing des options")
