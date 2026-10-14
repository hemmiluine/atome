import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Configuration de la page Streamlit ---
st.set_page_config(page_title="Simulation Lentille Convergente", layout="wide")
st.title("Construction de l'image par une lentille mince convergente")
st.markdown("Faites varier la position de l'objet et la distance focale pour observer l'évolution de l'image formée.")

# --- 2. Interface interactive (Sidebar) ---
st.sidebar.header("Paramètres Optiques")
xA = st.sidebar.slider("Position de l'objet $\\overline{OA}$ (en cm)", min_value=-25.0, max_value=-0.5, value=-15.0, step=0.5)
f = st.sidebar.slider("Distance focale $f'$ (en cm)", min_value=2.0, max_value=15.0, value=5.0, step=0.5)

yB_init = 3.0  # Hauteur algébrique de l'objet (AB en cm)

# --- 3. Calculs optiques ---
def calcul_image(xA, f):
    """
    Calcule la position et la taille de l'image avec gestion de l'objet au foyer.
    """
    # Tolérance pour la comparaison de flottants (xA = -f)
    if abs(xA + f) < 1e-5:
        return np.inf, np.inf  # L'image se forme à l'infini
    
    # Relation de conjugaison : 1/OA' = 1/OA + 1/f'
    xAp = (xA * f) / (xA + f)
    
    # Grandissement : gamma = A'B' / AB = OA' / OA
    gamma = xAp / xA
    yBp = gamma * yB_init
    
    return xAp, yBp

# --- 4. Fonction de tracé ---
def dessiner_optique(xA, f):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-30, 30)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_xlabel("Axe optique (cm)", fontsize=12)
    ax.set_ylabel("Hauteur (cm)", fontsize=12)
    
    # Axe optique
    ax.axhline(0, color='black', linewidth=1)
    
    # Lentille mince convergente (en x = 0)
    ax.axvline(0, color='blue', linewidth=2, label="Lentille convergente")
    ax.annotate('', xy=(0, 9.5), xytext=(0, 8.5), arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax.annotate('', xy=(0, -9.5), xytext=(0, -8.5), arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    
    # Points caractéristiques : O, F, F'
    ax.plot(0, 0, 'ko')
    ax.text(0.5, -1.2, 'O', fontsize=12)
    
    ax.plot(-f, 0, 'ro', label="Foyer objet F")
    ax.text(-f, -1.5, 'F', color='red', fontsize=12)
    
    ax.plot(f, 0, 'go', label="Foyer image F'")
    ax.text(f, -1.5, "F'", color='green', fontsize=12)
    
    # Tracé de l'objet AB
    ax.annotate('', xy=(xA, yB_init), xytext=(xA, 0), arrowprops=dict(color='orange', arrowstyle='->', lw=2))
    ax.text(xA, -1.5, 'A', color='orange', fontsize=12)
    ax.text(xA, yB_init + 0.5, 'B', color='orange', fontsize=12)
    
    xAp, yBp = calcul_image(xA, f)
    
    # --- Tracé des rayons lumineux ---
    if xAp != np.inf:
        # L'image se forme à distance finie
        ax.annotate('', xy=(xAp, yBp), xytext=(xAp, 0), arrowprops=dict(color='purple', arrowstyle='->', lw=2))
        ax.text(xAp, 0.5 if yBp < 0 else -1.5, "A'", color='purple', fontsize=12)
        ax.text(xAp, yBp - 1.5 if yBp < 0 else yBp + 0.5, "B'", color='purple', fontsize=12)
        
        # Rayon 1 (rouge)
        ax.plot([xA, 0], [yB_init, yB_init], 'r-', lw=1.5)
        ax.plot([0, xAp + (xAp)*0.2], [yB_init, yBp + (yBp - yB_init)*0.2], 'r-', lw=1.5)
        
        # Rayon 2 (vert)
        ax.plot([xA, xAp + (xAp - xA)*0.2], [yB_init, yBp + (yBp - yB_init)*0.2], 'g-', lw=1.5)
        
        # Pointillés si l'image est virtuelle
        if xAp < 0:
             ax.plot([0, xAp], [yB_init, yBp], 'r--', lw=1.5)
             ax.plot([0, xAp], [0, yBp], 'g--', lw=1.5)
    else:
        # Image à l'infini (xA = -f)
        ax.plot([xA, 0], [yB_init, yB_init], 'r-', lw=1.5)
        pente = -yB_init / f
        ax.plot([0, 30], [yB_init, yB_init + pente * 30], 'r-', lw=1.5)
        ax.plot([xA, 30], [yB_init, yB_init + pente * (30 - xA)], 'g-', lw=1.5)
        
        ax.text(5, 8, "L'image se forme à l'infini", fontsize=12, color='darkblue', bbox=dict(facecolor='white', alpha=0.8))

    ax.legend(loc='upper right')
    return fig, xAp, yBp

# --- 5. Affichage des résultats ---
fig, xAp, yBp = dessiner_optique(xA, f)

# Affichage du graphique matplotlib dans Streamlit
st.pyplot(fig)

# Affichage des valeurs numériques
st.subheader("Valeurs numériques")
col1, col2 = st.columns(2)

with col1:
    if xAp != np.inf:
        st.info(f"Position de l'image $\\overline{{OA'}}$ = **{xAp:.2f} cm**")
    else:
        st.info("Position de l'image $\\overline{OA'}$ = **$\\infty$**")

with col2:
    if xAp != np.inf:
        gamma = xAp / xA
        st.success(f"Grandissement $\\gamma$ = **{gamma:.2f}**")
    else:
        st.success("Grandissement $\\gamma$ non défini (image à l'infini)")
