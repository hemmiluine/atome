import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuration de la page Streamlit
st.set_page_config(page_title="Modèle Atomique par Sous-couches", layout="wide")

# Dictionnaire des 20 premiers éléments
ELEMENTS = {
    1: ('H', 'Hydrogène'), 2: ('He', 'Hélium'), 3: ('Li', 'Lithium'),
    4: ('Be', 'Béryllium'), 5: ('B', 'Bore'), 6: ('C', 'Carbone'),
    7: ('N', 'Azote'), 8: ('O', 'Oxygène'), 9: ('F', 'Fluor'),
    10: ('Ne', 'Néon'), 11: ('Na', 'Sodium'), 12: ('Mg', 'Magnésium'),
    13: ('Al', 'Aluminium'), 14: ('Si', 'Silicium'), 15: ('P', 'Phosphore'),
    16: ('S', 'Soufre'), 17: ('Cl', 'Chlore'), 18: ('Ar', 'Argon'),
    19: ('K', 'Potassium'), 20: ('Ca', 'Calcium')
}

def get_configuration(Z):
    """Calcule la répartition électronique par sous-couches jusqu'à Z=20."""
    config = {'1s': 0, '2s': 0, '2p': 0, '3s': 0, '3p': 0, '4s': 0}
    reste = Z
    
    if reste > 0: config['1s'] = min(reste, 2); reste -= config['1s']
    if reste > 0: config['2s'] = min(reste, 2); reste -= config['2s']
    if reste > 0: config['2p'] = min(reste, 6); reste -= config['2p']
    if reste > 0: config['3s'] = min(reste, 2); reste -= config['3s']
    if reste > 0: config['3p'] = min(reste, 6); reste -= config['3p']
    if reste > 0: config['4s'] = min(reste, 2); reste -= config['4s']
    
    return config

def dessiner_atome(Z, symbole, nom):
    """Génère le graphique Matplotlib avec l'esthétique demandée."""
    config = get_configuration(Z)
    
    # Création de la figure avec fond gris clair
    couleur_fond = '#eaeaea'
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor(couleur_fond)
    ax.set_facecolor(couleur_fond)
    
    # Représentation du noyau (cercle orange)
    noyau = plt.Circle((0, 0), 0.6, color='#ea8c00', zorder=5)
    ax.add_patch(noyau)
    ax.text(0, 0, f"Noyau\n{symbole}", color='#333333', fontsize=12, 
            ha='center', va='center', fontweight='bold', zorder=6)
    
    # Propriétés visuelles des sous-couches : (rayon, couleur, angle_label_deg)
    # Les sous-couches d'une même couche (K, L, M...) ont la même couleur.
    couches_meta = {
        '1s': {'r': 2.0, 'color': '#007acc', 'label_angle': 70, 'couche': 'K'}, # Bleu
        '2s': {'r': 3.2, 'color': '#75a82b', 'label_angle': 60, 'couche': 'L'}, # Vert
        '2p': {'r': 3.6, 'color': '#75a82b', 'label_angle': 75, 'couche': 'L'},
        '3s': {'r': 4.8, 'color': '#9b59b6', 'label_angle': 50, 'couche': 'M'}, # Violet
        '3p': {'r': 5.2, 'color': '#9b59b6', 'label_angle': 65, 'couche': 'M'},
        '4s': {'r': 6.4, 'color': '#e74c3c', 'label_angle': 45, 'couche': 'N'}  # Rouge
    }
    
    max_radius = 1
    
    # Tracé des orbites et des électrons
    for sous_couche, nb_e in config.items():
        if nb_e > 0:
            meta = couches_meta[sous_couche]
            r = meta['r']
            couleur = meta['color']
            max_radius = max(max_radius, r)
            
            # Dessin de l'orbite (trait continu plein)
            cercle = plt.Circle((0, 0), r, color=couleur, fill=False, linewidth=1.5, zorder=1)
            ax.add_patch(cercle)
            
            # Ajout de l'étiquette (ex: '1s') avec un fond blanc pour la lisibilité
            angle_rad_label = np.radians(meta['label_angle'])
            x_label = r * np.cos(angle_rad_label)
            y_label = r * np.sin(angle_rad_label)
            ax.text(x_label, y_label, sous_couche, color=couleur, fontsize=14, 
                    ha='center', va='center', fontweight='bold',
                    bbox=dict(facecolor='white', edgecolor='none', pad=2, alpha=0.9), zorder=2)
            
            # Calcul de la position des électrons
            # Un petit décalage (offset) évite que tous les électrons soient alignés sur l'axe X
            offset_angle = np.pi / 4 if sous_couche.endswith('s') else 0
            angles = np.linspace(0, 2 * np.pi, nb_e, endpoint=False) + offset_angle
            x_e = r * np.cos(angles)
            y_e = r * np.sin(angles)
            
            # Dessin des électrons (gros points gris foncé/noirs)
            ax.plot(x_e, y_e, 'o', color='#2b2b2b', markersize=14, zorder=4)

    # Paramétrage final de la zone de dessin
    limite = max_radius + 1
    ax.set_aspect('equal')
    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)
    ax.axis('off')
    plt.tight_layout()
    
    return fig

# --- INTERFACE UTILISATEUR STREAMLIT ---

st.sidebar.title("⚛️ Configuration")
liste_choix = [f"{Z} - {nom} ({symbole})" for Z, (symbole, nom) in ELEMENTS.items()]
choix = st.sidebar.selectbox("Sélectionne un atome (Z=1 à 20) :", liste_choix, index=5) # Carbone (Z=6) par défaut

Z_choisi = int(choix.split(" - ")[0])
symbole_choisi, nom_choisi = ELEMENTS[Z_choisi]
config = get_configuration(Z_choisi)

st.title(f"Atome de {nom_choisi} ({symbole_choisi}, Z={Z_choisi})")

col_gauche, col_droite = st.columns([2, 1])

# Colonne Gauche : Modèle visuel
with col_gauche:
    fig = dessiner_atome(Z_choisi, symbole_choisi, nom_choisi)
    st.pyplot(fig)

# Colonne Droite : Explications pédagogiques
with col_droite:
    st.subheader(f"Configuration Électronique")
    
    # Regroupement par couches principales (K, L, M, N)
    if config['1s'] > 0:
        st.markdown("**Couche K (n=1)** :")
        st.markdown(f"- Sous-couche 1s ({config['1s']} e⁻)")
        
    if config['2s'] > 0 or config['2p'] > 0:
        st.markdown("**Couche L (n=2)** :")
        if config['2s'] > 0: st.markdown(f"- Sous-couche 2s ({config['2s']} e⁻)")
        if config['2p'] > 0: st.markdown(f"- Sous-couche 2p ({config['2p']} e⁻)")
        
    if config['3s'] > 0 or config['3p'] > 0:
        st.markdown("**Couche M (n=3)** :")
        if config['3s'] > 0: st.markdown(f"- Sous-couche 3s ({config['3s']} e⁻)")
        if config['3p'] > 0: st.markdown(f"- Sous-couche 3p ({config['3p']} e⁻)")
        
    if config['4s'] > 0:
        st.markdown("**Couche N (n=4)** :")
        st.markdown(f"- Sous-couche 4s ({config['4s']} e⁻)")

    st.info("💡 **Principe de construction**\n\n"
            "Ce modèle montre comment les électrons remplissent "
            "progressivement les sous-couches (s, p...) qui composent "
            "les grandes couches principales (K, L, M...). "
            "Les orbites rapprochées et de même couleur appartiennent à la même couche principale.")
