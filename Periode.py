import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# --- Configuration de la page Streamlit ---
st.set_page_config(page_title="Périodicité d'une Onde", layout="wide")
st.title("🌊 Périodicité Spatiale et Temporelle")

# --- Barre latérale pour les contrôles interactifs ---
st.sidebar.header("Paramètres de l'onde")
T = st.sidebar.slider("Période Temporelle T (s)", 1.0, 10.0, 3.0, 0.1)
lam = st.sidebar.slider(r"Période Spatiale $\lambda$ (m)", 1.0, 10.0, 4.0, 0.1)

st.sidebar.markdown("---")
animation_auto = st.sidebar.checkbox("Lancer l'animation automatique", value=False)
# Si pas d'animation auto, l'élève défile le temps manuellement (très pédagogique)
t_manuel = st.sidebar.slider("Défilement manuel du temps (s)", 0.0, 15.0, 0.0, 0.1) if not animation_auto else 0

# --- Paramètres de base ---
Um = 2.0
phi = 0
t_max = 15
x_vals = np.linspace(0, 15, 500)
t_vals = np.linspace(0, t_max, 500)

def u(x, t):
    return Um * np.cos(2 * np.pi * (t / T - x / lam) + phi)

# Espace vide qui sera mis à jour avec les graphiques
zone_graphique = st.empty()

# --- Fonction de tracé ---
def tracer_graphiques(t_actuel):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.subplots_adjust(hspace=0.4)

    # Vue spatiale
    ax1.plot(x_vals, u(x_vals, t_actuel), color='#1f77b4', lw=2)
    ax1.plot(0, u(0, t_actuel), marker='o', color='red', ms=8)
    ax1.set_title(f"Vue Spatiale (Onde à l'instant t = {t_actuel:.1f} s)")
    ax1.set_xlabel("Position x (m)")
    ax1.set_ylabel("Amplitude")
    ax1.set_xlim(0, 15)
    ax1.set_ylim(-Um * 1.5, Um * 1.5)
    ax1.grid(True, linestyle='--')

    # Vue temporelle
    t_hist = t_vals[t_vals <= t_actuel]
    u_hist = u(0, t_hist)
    ax2.plot(t_hist, u_hist, color='red', lw=2)
    ax2.plot(t_actuel, u(0, t_actuel), marker='o', color='red', ms=8)
    ax2.set_title("Vue Temporelle (Historique du point x=0)")
    ax2.set_xlabel("Temps t (s)")
    ax2.set_ylabel("Amplitude")
    ax2.set_xlim(0, t_max)
    ax2.set_ylim(-Um * 1.5, Um * 1.5)
    ax2.grid(True, linestyle='--')

    return fig

# --- Moteur d'affichage ---
if animation_auto:
    # Boucle pour simuler l'animation en direct
    for t in np.arange(0, t_max, 0.1):
        fig = tracer_graphiques(t)
        zone_graphique.pyplot(fig)
        plt.close(fig) # Indispensable pour ne pas surcharger la mémoire du serveur
        time.sleep(0.05)
else:
    # Affichage statique contrôlé par le curseur manuel
    fig = tracer_graphiques(t_manuel)
    zone_graphique.pyplot(fig)
    plt.close(fig)
