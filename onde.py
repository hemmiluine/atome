import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuration
st.set_page_config(page_title="Onde Électromagnétique", layout="wide")
st.title("Propagation d'une Onde Électromagnétique 🌊")
st.markdown("Animation 3D fluide (rendu natif Plotly).")

# --- Panneau de contrôle latéral ---
st.sidebar.header("Paramètres Physiques")
lam = st.sidebar.slider("Période spatiale (Longueur d'onde λ)", 2.0, 15.0, 6.0, 0.5)
T = st.sidebar.slider("Période temporelle (T)", 1.0, 10.0, 4.0, 0.5)

st.sidebar.header("Vitesse d'affichage")
st.sidebar.info("L'animation se lance via le bouton 'Lecture' situé sur le graphique.")
# Permet de ralentir la transition entre les images (en millisecondes)
vitesse = st.sidebar.slider("Vitesse du ralenti (ms/image)", min_value=10, max_value=200, value=40, step=10)

# --- Préparation des calculs mathématiques ---
x = np.linspace(0, 25, 250)

def generate_vectors(x_array, phase_array, is_electric):
    field = np.sin(phase_array)
    x_v, y_v, z_v = [], [], []
    step = 8
    for i in range(0, len(x_array), step):
        x_v.extend([x_array[i], x_array[i], None])
        if is_electric:
            y_v.extend([0, field[i], None])
            z_v.extend([0, 0, None])
        else:
            y_v.extend([0, 0, None])
            z_v.extend([0, field[i], None])
    return field, x_v, y_v, z_v

# --- Génération des images (frames) de l'animation ---
# On calcule une seule période temporelle complète découpée en 40 images.
# Plotly va les lire en boucle continuellement.
# --- Génération des images (frames) de l'animation ---
# On calcule plusieurs périodes pour que l'animation dure beaucoup plus longtemps
nb_cycles = 15  # L'onde effectuera 15 oscillations avant de s'arrêter (modifiable)
images_par_cycle = 30 # 30 images par oscillation garantit une bonne fluidité sans surcharger la mémoire
total_frames = nb_cycles * images_par_cycle

# On étire le temps calculé sur le nombre total de cycles souhaité
t_values = np.linspace(0, nb_cycles * T, total_frames, endpoint=False)
frames = []

for k, t in enumerate(t_values):
    phase = 2 * np.pi * (x / lam - t / T)
    E, xE_v, yE_v, zE_v = generate_vectors(x, phase, is_electric=True)
    B, xB_v, yB_v, zB_v = generate_vectors(x, phase, is_electric=False)
    
    # On met à jour les 4 courbes (enveloppes + vecteurs)
    frames.append(go.Frame(
        data=[
            go.Scatter3d(x=x, y=E, z=np.zeros_like(x)),
            go.Scatter3d(x=xE_v, y=yE_v, z=zE_v),
            go.Scatter3d(x=x, y=np.zeros_like(x), z=B),
            go.Scatter3d(x=xB_v, y=yB_v, z=zB_v)
        ],
        name=f"frame_{k}"
    ))

# --- Tracé initial (t=0) ---
phase0 = 2 * np.pi * (x / lam)
E0, xE0, yE0, zE0 = generate_vectors(x, phase0, True)
B0, xB0, yB0, zB0 = generate_vectors(x, phase0, False)

fig = go.Figure(
    data=[
        go.Scatter3d(x=x, y=E0, z=np.zeros_like(x), mode='lines', line=dict(color='red', width=4), name='Champ E'),
        go.Scatter3d(x=xE0, y=yE0, z=zE0, mode='lines', line=dict(color='rgba(255,0,0,0.5)', width=2), showlegend=False),
        go.Scatter3d(x=x, y=np.zeros_like(x), z=B0, mode='lines', line=dict(color='blue', width=4), name='Champ B'),
        go.Scatter3d(x=xB0, y=yB0, z=zB0, mode='lines', line=dict(color='rgba(0,0,255,0.5)', width=2), showlegend=False),
        go.Scatter3d(x=[0, 25], y=[0, 0], z=[0, 0], mode='lines', line=dict(color='black', width=2, dash='dash'), name='Axe x')
    ],
    frames=frames
)

# --- Configuration de la scène 3D et des boutons interactifs ---
fig.update_layout(
    scene=dict(
        xaxis=dict(title='x', range=[0, 25], autorange=False, showbackground=False),
        yaxis=dict(title='y (E)', range=[-1.5, 1.5], autorange=False, showbackground=False),
        zaxis=dict(title='z (B)', range=[-1.5, 1.5], autorange=False, showbackground=False),
        camera=dict(eye=dict(x=-1.2, y=-1.5, z=1.2))
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=650,
    # Ajout des contrôles Play/Pause natifs à Plotly
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        y=1.0, x=0.0,
        xanchor="left", yanchor="top",
        buttons=[
            dict(label="▶ Lecture",
                 method="animate",
                 args=[None, dict(frame=dict(duration=vitesse, redraw=True), 
                                  fromcurrent=True, mode="immediate",
                                  transition=dict(duration=0))]),
            dict(label="⏸ Pause",
                 method="animate",
                 args=[[None], dict(frame=dict(duration=0, redraw=False), 
                                    mode="immediate", transition=dict(duration=0))])
        ]
    )]
)

# Affichage final dans Streamlit
st.plotly_chart(fig, use_container_width=True)
