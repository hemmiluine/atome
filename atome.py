import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Dictionnaire des 20 premiers éléments : {Z: ('Symbole', 'Nom')}
ELEMENTS = {
    1: ('H', 'Hydrogène'), 2: ('He', 'Hélium'), 3: ('Li', 'Lithium'),
    4: ('Be', 'Béryllium'), 5: ('B', 'Bore'), 6: ('C', 'Carbone'),
    7: ('N', 'Azote'), 8: ('O', 'Oxygène'), 9: ('F', 'Fluor'),
    10: ('Ne', 'Néon'), 11: ('Na', 'Sodium'), 12: ('Mg', 'Magnésium'),
    13: ('Al', 'Aluminium'), 14: ('Si', 'Silicium'), 15: ('P', 'Phosphore'),
    16: ('S', 'Soufre'), 17: ('Cl', 'Chlore'), 18: ('Ar', 'Argon'),
    19: ('K', 'Potassium'), 20: ('Ca', 'Calcium')
}

def calculer_couches(Z):
    """Calcule la répartition électronique jusqu'à Z=20."""
    couches = [0, 0, 0, 0]
    if Z <= 2:
        couches[0] = Z
    elif Z <= 10:
        couches[0] = 2
        couches[1] = Z - 2
    elif Z <= 18:
        couches[0] = 2
        couches[1] = 8
        couches[2] = Z - 10
    elif Z <= 20:
        couches[0] = 2
        couches[1] = 8
        couches[2] = 8
        couches[3] = Z - 18
    return couches

def dessiner_atome(Z, symbole, nom):
    """Génère la figure matplotlib du modèle atomique."""
    couches = calculer_couches(Z)
    
    fig, ax = plt.subplots(figsize=(7, 7))
    
    # Noyau
    ax.plot(0, 0, 'ro', markersize=20, label=f'Noyau ({symbole})')
    ax.text(0, 0, symbole, color='white', fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Paramètres des couches (jusqu'à 4 couches)
    rayons = [1.5, 2.5, 3.5, 4.5]
    couleurs_electrons = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']
    noms_couches = ['Couche 1 (1s)', 'Couche 2 (2s, 2p)', 'Couche 3 (3s, 3p)', 'Couche 4 (4s)']
    
    # Placement des électrons
    for i, nb_e in enumerate(couches):
        if nb_e > 0:
            # Orbite
            cercle = plt.Circle((0, 0), rayons[i], color='gray', fill=False, linestyle='--', alpha=0.5)
            ax.add_patch(cercle)
            
            # Position des électrons
            angles = np.linspace(0, 2 * np.pi, nb_e, endpoint=False)
            x_e = rayons[i] * np.cos(angles)
            y_e = rayons[i] * np.sin(angles)
            
            ax.plot(x_e, y_e, 'o', color=couleurs_electrons[i], markersize=10, 
                    label=f'{nb_e} e- sur {noms_couches[i]}')

    # Mise en forme
    ax.set_aspect('equal')
    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-5.5, 5.5)
    ax.axis('off')
    
    plt.title(f"Modèle de l'atome de {nom} (Z={Z})", fontsize=16, pad=20)
    # Ajustement de la légende pour éviter qu'elle soit coupée dans Streamlit
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=2)
    plt.tight_layout()
    
    return fig

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Modèle Atomique", layout="centered")

st.title("⚛️ Modélisation du cortège électronique")
st.markdown("Choisis un atome pour visualiser la répartition de ses électrons par couche.")

# Création de la liste déroulante pour le choix de l'atome
liste_choix = [f"{Z} - {nom} ({symbole})" for Z, (symbole, nom) in ELEMENTS.items()]
choix_utilisateur = st.selectbox("Sélectionne un élément (Z=1 à 20) :", liste_choix, index=7) # Oxygène par défaut

# Extraction du Z à partir du choix
Z_choisi = int(choix_utilisateur.split(" - ")[0])
symbole_choisi, nom_choisi = ELEMENTS[Z_choisi]

# Affichage du graphique et de la configuration textuelle
col1, col2 = st.columns([2, 1])

with col1:
    fig = dessiner_atome(Z_choisi, symbole_choisi, nom_choisi)
    st.pyplot(fig)

with col2:
    st.subheader("Configuration")
    couches_calc = calculer_couches(Z_choisi)
    st.write(f"**Numéro atomique Z :** {Z_choisi}")
    st.write(f"**Électrons totaux :** {Z_choisi}")
    
    # Affichage de la structure électronique sous forme de texte (ex: 1s² 2s² 2p⁶)
    st.markdown("### Répartition")
    if couches_calc[0] > 0: st.write(f"- **Couche 1** : {couches_calc[0]} e⁻")
    if couches_calc[1] > 0: st.write(f"- **Couche 2** : {couches_calc[1]} e⁻")
    if couches_calc[2] > 0: st.write(f"- **Couche 3** : {couches_calc[2]} e⁻")
    if couches_calc[3] > 0: st.write(f"- **Couche 4** : {couches_calc[3]} e⁻")
