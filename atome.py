import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

st.set_page_config(page_title="Modèle Atomique", layout="wide")

ELEMENTS = {
    1: ('H', 'Hydrogène', 0), 2: ('He', 'Hélium', 2), 3: ('Li', 'Lithium', 4),
    4: ('Be', 'Béryllium', 5), 5: ('B', 'Bore', 6), 6: ('C', 'Carbone', 6),
    7: ('N', 'Azote', 7), 8: ('O', 'Oxygène', 8), 9: ('F', 'Fluor', 10),
    10: ('Ne', 'Néon', 10), 11: ('Na', 'Sodium', 12), 12: ('Mg', 'Magnésium', 12),
    13: ('Al', 'Aluminium', 14), 14: ('Si', 'Silicium', 14), 15: ('P', 'Phosphore', 16),
    16: ('S', 'Soufre', 16), 17: ('Cl', 'Chlore', 18), 18: ('Ar', 'Argon', 22),
    19: ('K', 'Potassium', 20), 20: ('Ca', 'Calcium', 20)
}

def get_configuration(Z):
    config = {'1s': 0, '2s': 0, '2p': 0, '3s': 0, '3p': 0, '4s': 0}
    reste = Z
    if reste > 0: config['1s'] = min(reste, 2); reste -= config['1s']
    if reste > 0: config['2s'] = min(reste, 2); reste -= config['2s']
    if reste > 0: config['2p'] = min(reste, 6); reste -= config['2p']
    if reste > 0: config['3s'] = min(reste, 2); reste -= config['3s']
    if reste > 0: config['3p'] = min(reste, 6); reste -= config['3p']
    if reste > 0: config['4s'] = min(reste, 2); reste -= config['4s']
    return config

def dessiner_atome(Z, N, symbole, nom, niveau):
    config = get_configuration(Z)
    couleur_fond = '#eaeaea'
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor(couleur_fond)
    ax.set_facecolor(couleur_fond)
    
    # Noyau (commun aux deux niveaux)
    particules = ['p'] * Z + ['n'] * N
    random.seed(42)
    random.shuffle(particules)
    golden_angle = np.pi * (3 - np.sqrt(5))
    
    for i, p in enumerate(particules):
        r_nucleon = 0.13 * np.sqrt(i) 
        theta = i * golden_angle
        x, y = r_nucleon * np.cos(theta), r_nucleon * np.sin(theta)
        couleur = '#ff4d4d' if p == 'p' else '#85929e'
        bordure = '#cc0000' if p == 'p' else '#5d6d7e'
        ax.add_patch(plt.Circle((x, y), 0.10, color=couleur, ec=bordure, lw=0.5, zorder=5))

    r_max_noyau = 0.13 * np.sqrt(len(particules)) if particules else 0
    ax.text(0, r_max_noyau + 0.3, f"Noyau\n{symbole}", color='#333333', fontsize=12, 
            ha='center', va='center', fontweight='bold', zorder=6,
            bbox=dict(facecolor=couleur_fond, edgecolor='none', pad=1, alpha=0.7))

    max_radius = 2.5

    # Affichage conditionnel selon le niveau
    if niveau == "Collège":
        r = 5.0
        max_radius = r
        # Orbite unique
        ax.add_patch(plt.Circle((0, 0), r, color='#7f8c8d', fill=False, linewidth=1.5, zorder=1))
        # Étiquette
        ax.text(0, r, "Nuage électronique", color='#7f8c8d', fontsize=14, 
                ha='center', va='center', fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', pad=2, alpha=0.9), zorder=2)
        # Placement de tous les électrons sur la même orbite
        angles = np.linspace(0, 2 * np.pi, Z, endpoint=False)
        x_e, y_e = r * np.cos(angles), r * np.sin(angles)
        ax.plot(x_e, y_e, 'o', color='#2b2b2b', markersize=12, zorder=4)

    else:
        # Affichage Lycée (sous-couches)
        couches_meta = {
            '1s': {'r': 2.5, 'color': '#007acc', 'label_angle': 70},
            '2s': {'r': 3.7, 'color': '#75a82b', 'label_angle': 60},
            '2p': {'r': 4.1, 'color': '#75a82b', 'label_angle': 75},
            '3s': {'r': 5.3, 'color': '#9b59b6', 'label_angle': 50},
            '3p': {'r': 5.7, 'color': '#9b59b6', 'label_angle': 65},
            '4s': {'r': 6.9, 'color': '#e74c3c', 'label_angle': 45}
        }
        
        for sous_couche, nb_e in config.items():
            if nb_e > 0:
                meta = couches_meta[sous_couche]
                r, couleur = meta['r'], meta['color']
                max_radius = max(max_radius, r)
                
                ax.add_patch(plt.Circle((0, 0), r, color=couleur, fill=False, linewidth=1.5, zorder=1))
                
                angle_rad = np.radians(meta['label_angle'])
                ax.text(r * np.cos(angle_rad), r * np.sin(angle_rad), sous_couche, color=couleur, 
                        fontsize=14, ha='center', va='center', fontweight='bold',
                        bbox=dict(facecolor='white', edgecolor='none', pad=2, alpha=0.9), zorder=2)
                
                offset = np.pi / 4 if sous_couche.endswith('s') else 0
                angles = np.linspace(0, 2 * np.pi, nb_e, endpoint=False) + offset
                ax.plot(r * np.cos(angles), r * np.sin(angles), 'o', color='#2b2b2b', markersize=12, zorder=4)

    limite = max_radius + 1.2
    ax.set_aspect('equal')
    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)
    ax.axis('off')
    plt.tight_layout()
    return fig

# --- INTERFACE ---
st.sidebar.title("⚛️ Configuration")
niveau = st.sidebar.radio("Niveau scolaire :", ["Collège (Orbite unique)", "Lycée (Sous-couches)"])
st.sidebar.markdown("---")
liste_choix = [f"{Z} - {nom} ({symbole})" for Z, (symbole, nom, N) in ELEMENTS.items()]
choix = st.sidebar.selectbox("Sélectionne un atome :", liste_choix, index=15)

Z_choisi = int(choix.split(" - ")[0])
symbole_choisi, nom_choisi, N_choisi = ELEMENTS[Z_choisi]
A_masse = Z_choisi + N_choisi

st.title(f"Atome de {nom_choisi} ({symbole_choisi})")
st.markdown(f"**Isotope principal :** Masse A = {A_masse} | Numéro atomique Z = {Z_choisi}")

col_gauche, col_droite = st.columns([2, 1])

with col_gauche:
    fig = dessiner_atome(Z_choisi, N_choisi, symbole_choisi, nom_choisi, niveau.split()[0])
    st.pyplot(fig)
    st.markdown("""
    <div style='display: flex; justify-content: center; gap: 20px;'>
        <div><span style='color: #ff4d4d;'>●</span> <b>Protons (p⁺)</b></div>
        <div><span style='color: #85929e;'>●</span> <b>Neutrons (n⁰)</b></div>
        <div><span style='color: #2b2b2b;'>●</span> <b>Électrons (e⁻)</b></div>
    </div>
    """, unsafe_allow_html=True)

with col_droite:
    st.subheader("Composition du Noyau")
    st.write(f"- **{Z_choisi}** Protons (charge +)")
    st.write(f"- **{N_choisi}** Neutrons (charge 0)")
    st.write(f"- Nucléons totaux (A) : **{A_masse}**")

    st.markdown("---")
    st.subheader("Cortège Électronique")
    
    if niveau.startswith("Collège"):
        st.write(f"L'atome est électriquement neutre. Il possède autant d'électrons que de protons.")
        st.write(f"- **Électrons totaux : {Z_choisi}**")
    else:
        config = get_configuration(Z_choisi)
        if config['1s'] > 0:
            st.markdown("**Couche K (n=1)** :\n- Sous-couche 1s (" + str(config['1s']) + " e⁻)")
        if config['2s'] > 0 or config['2p'] > 0:
            st.markdown("**Couche L (n=2)** :")
            if config['2s'] > 0: st.markdown(f"- Sous-couche 2s ({config['2s']} e⁻)")
            if config['2p'] > 0: st.markdown(f"- Sous-couche 2p ({config['2p']} e⁻)")
        if config['3s'] > 0 or config['3p'] > 0:
            st.markdown("**Couche M (n=3)** :")
            if config['3s'] > 0: st.markdown(f"- Sous-couche 3s ({config['3s']} e⁻)")
            if config['3p'] > 0: st.markdown(f"- Sous-couche 3p ({config['3p']} e⁻)")
        if config['4s'] > 0:
            st.markdown(f"**Couche N (n=4)** :\n- Sous-couche 4s ({config['4s']} e⁻)")
