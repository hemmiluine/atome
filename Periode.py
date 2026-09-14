import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import streamlit.components.v1 as components

st.set_page_config(page_title="Périodicité d'une Onde", layout="wide")
st.title("🌊 Périodicité Spatiale et Temporelle")

# --- Barre latérale ---
st.sidebar.header("Paramètres de l'onde")
st.sidebar.write("Modifiez les paramètres ci-dessous pour regénérer l'animation :")
T = st.sidebar.slider("Période Temporelle T (s)", 1.0, 10.0, 3.0, 0.1)
lam = st.sidebar.slider(r"Période Spatiale $\lambda$ (m)", 1.0, 10.0, 4.0, 0.1)

# --- Paramètres de base ---
Um = 2.0
phi = 0
t_max = 15
x_vals = np.linspace(0, 15, 500)
t_vals = np.linspace(0, t_max, 500)

def u(x, t):
    return Um * np.cos(2 * np.pi * (t / T - x / lam) + phi)

# --- Préparation de la figure Matplotlib ---
# On utilise un "spinner" pendant que le serveur génère la vidéo
with st.spinner("Génération de l'animation en cours (cela peut prendre quelques secondes)..."):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.subplots_adjust(hspace=0.4)

    # 1. Vue spatiale
    ligne_spatiale, = ax1.plot(x_vals, u(x_vals, 0), color='#1f77b4', lw=2)
    point_fixe_spatial, = ax1.plot(0, u(0, 0), marker='o', color='red', ms=8)
    ax1.set_title("Vue Spatiale (Onde à l'instant t)")
    ax1.set_xlabel("Position x (m)")
    ax1.set_ylabel("Amplitude")
    ax1.set_xlim(0, 15)
    ax1.set_ylim(-Um * 1.5, Um * 1.5)
    ax1.grid(True, linestyle='--')

    # 2. Vue temporelle
    ligne_temporelle, = ax2.plot([], [], color='red', lw=2)
    point_actuel_temporel, = ax2.plot([], [], marker='o', color='red', ms=8)
    ax2.set_title("Vue Temporelle (Historique du point x=0)")
    ax2.set_xlabel("Temps t (s)")
    ax2.set_ylabel("Amplitude")
    ax2.set_xlim(0, t_max)
    ax2.set_ylim(-Um * 1.5, Um * 1.5)
    ax2.grid(True, linestyle='--')

    # --- Fonction de mise à jour pour l'animation ---
    def update(frame):
        # On calcule le temps actuel basé sur le numéro de la frame
        t_actuel = frame * (t_max / 100) 
        
        ligne_spatiale.set_ydata(u(x_vals, t_actuel))
        point_fixe_spatial.set_ydata([u(0, t_actuel)])
        
        t_hist = t_vals[t_vals <= t_actuel]
        u_hist = u(0, t_hist)
        ligne_temporelle.set_data(t_hist, u_hist)
        point_actuel_temporel.set_data([t_actuel], [u(0, t_actuel)])
        
        return ligne_spatiale, point_fixe_spatial, ligne_temporelle, point_actuel_temporel

    # On limite à 100 frames pour que la génération côté serveur reste rapide
    ani = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=False)

    # --- Injection de l'animation HTML dans Streamlit ---
    # to_jshtml() crée un lecteur vidéo interactif en pur JavaScript !
    components.html(ani.to_jshtml(), height=850)
    
    plt.close(fig) # Libère la mémoire
