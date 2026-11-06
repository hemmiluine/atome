import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# Configuration de la page
st.set_page_config(page_title="Onde Électromagnétique", layout="wide")

# Initialisation du temps dans la mémoire de session (permet l'animation)
if "t" not in st.session_state:
    st.session_state.t = 0.0

st.title("Propagation d'une Onde Électromagnétique 🌊")
st.markdown(
    "Visualisation 3D d'une onde plane progressive monochromatique se déplaçant selon l'axe $x$. "
    "Les champs électrique $\\vec{E}$ et magnétique $\\vec{B}$ sont en phase et orthogonaux."
)

# --- Panneau de contrôle latéral ---
st.sidebar.header("Paramètres Physiques")
lam = st.sidebar.slider(
    "Période spatiale (Longueur d'onde λ)", 
    min_value=2.0, max_value=15.0, value=6.0, step=0.5,
    help="Distance sur laquelle le motif de l'onde se répète à un instant donné."
)

T = st.sidebar.slider(
    "Période temporelle (T)", 
    min_value=1.0, max_value=10.0, value=4.0, step=0.5,
    help="Durée nécessaire pour que l'onde effectue un cycle complet en un point donné."
)

st.sidebar.header("Contrôle de l'Animation")
dt = st.sidebar.slider(
    "Vitesse d'écoulement du temps (dt)", 
    min_value=0.01, max_value=0.30, value=0.05, step=0.01,
    help="Diminuez cette valeur pour ralentir l'animation du temps."
)

is_playing = st.sidebar.checkbox("Lecture / Pause", value=True)

if st.sidebar.button("Réinitialiser le temps à t=0"):
    st.session_state.t = 0.0

# --- Calculs Mathématiques ---
x = np.linspace(0, 25, 250) # Axe de propagation fixe
phase = 2 * np.pi * (x / lam - st.session_state.t / T)

# Equations de l'onde : E = E0 * sin(kx - ωt) et B = B0 * sin(kx - ωt)
E = np.sin(phase) 
B = np.sin(phase) 

# Fonction utilitaire pour générer les lignes des vecteurs (pour l'aspect visuel "peigne")
def generate_vectors(x_array, field_array, is_electric):
    x_vec, y_vec, z_vec = [], [], []
    step = 8 # Affiche un vecteur tous les 8 points pour éviter la surcharge
    for i in range(0, len(x_array), step):
        x_vec.extend([x_array[i], x_array[i], None])
        if is_electric:
            y_vec.extend([0, field_array[i], None])
            z_vec.extend([0, 0, None])
        else:
            y_vec.extend([0, 0, None])
            z_vec.extend([0, field_array[i], None])
    return x_vec, y_vec, z_vec

xE_v, yE_v, zE_v = generate_vectors(x, E, is_electric=True)
xB_v, yB_v, zB_v = generate_vectors(x, B, is_electric=False)

# --- Construction de la figure Plotly ---
fig = go.Figure()

# Enveloppe et vecteurs du champ Électrique (E) - Plan XY
fig.add_trace(go.Scatter3d(x=x, y=E, z=np.zeros_like(x), mode='lines', 
                           line=dict(color='red', width=4), name='Champ Électrique (E)'))
fig.add_trace(go.Scatter3d(x=xE_v, y=yE_v, z=zE_v, mode='lines', 
                           line=dict(color='rgba(255,0,0,0.5)', width=2), showlegend=False))

# Enveloppe et vecteurs du champ Magnétique (B) - Plan XZ
fig.add_trace(go.Scatter3d(x=x, y=np.zeros_like(x), z=B, mode='lines', 
                           line=dict(color='blue', width=4), name='Champ Magnétique (B)'))
fig.add_trace(go.Scatter3d(x=xB_v, y=yB_v, z=zB_v, mode='lines', 
                           line=dict(color='rgba(0,0,255,0.5)', width=2), showlegend=False))

# Axe de propagation
fig.add_trace(go.Scatter3d(x=[0, 25], y=[0, 0], z=[0, 0], mode='lines', 
                           line=dict(color='black', width=2, dash='dash'), name='Axe de propagation'))

# Mise en page de la scène 3D
fig.update_layout(
    scene=dict(
        xaxis=dict(title='x (Distance)', range=[0, 25], showbackground=False),
        yaxis=dict(title='y (Champ E)', range=[-1.5, 1.5], showbackground=False),
        zaxis=dict(title='z (Champ B)', range=[-1.5, 1.5], showbackground=False),
        camera=dict(eye=dict(x=-1.2, y=-1.5, z=1.2)) # Angle de vue optimisé
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=650,
    legend=dict(x=0, y=1)
)

# Affichage du graphique
st.plotly_chart(fig, use_container_width=True)

# Affichage du temps actuel
st.metric("Temps écoulé (t)", f"{st.session_state.t:.2f} s")

# --- Boucle d'animation Streamlit ---
if is_playing:
    st.session_state.t += dt
    time.sleep(0.05) # Limite le taux de rafraîchissement pour éviter de saturer le processeur
    st.rerun()       # Relance l'exécution du script pour afficher la frame suivante
