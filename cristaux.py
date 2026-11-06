import streamlit as st
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Cristallographie 3D - ENS", layout="wide")

st.title("🧊 Modèles Cristallins 3D (Enseignement Scientifique)")
st.markdown("Visualisez les mailles cristallines et comprenez la **multiplicité** (le compte des atomes par maille).")

# Fonction pour dessiner les arêtes du cube
def get_cube_edges():
    return [
        ([0, 1], [0, 0], [0, 0]), ([0, 1], [1, 1], [0, 0]),
        ([0, 1], [0, 0], [1, 1]), ([0, 1], [1, 1], [1, 1]),
        ([0, 0], [0, 1], [0, 0]), ([1, 1], [0, 1], [0, 0]),
        ([0, 0], [0, 1], [1, 1]), ([1, 1], [0, 1], [1, 1]),
        ([0, 0], [0, 0], [0, 1]), ([1, 1], [0, 0], [0, 1]),
        ([0, 0], [1, 1], [0, 1]), ([1, 1], [1, 1], [0, 1])
    ]

# Génération de la figure 3D
def plot_structure(structure_type):
    fig = go.Figure()

    # 1. Dessin des arêtes de la maille (cube)
    for edge in get_cube_edges():
        fig.add_trace(go.Scatter3d(
            x=edge[0], y=edge[1], z=edge[2], 
            mode='lines', line=dict(color='black', width=3), 
            showlegend=False, hoverinfo='skip'
        ))

    # 2. Atomes aux sommets (communs à toutes les structures cubiques)
    corners_x = [0, 1, 1, 0, 0, 1, 1, 0]
    corners_y = [0, 0, 1, 1, 0, 0, 1, 1]
    corners_z = [0, 0, 0, 0, 1, 1, 1, 1]

    fig.add_trace(go.Scatter3d(
        x=corners_x, y=corners_y, z=corners_z,
        mode='markers',
        marker=dict(size=35, color='#EF553B', opacity=0.9, symbol='circle'),
        name="Sommets (partagés en 8)",
        hovertemplate="Sommet<extra></extra>"
    ))

    # 3. Ajout des atomes spécifiques selon le type de maille
    if structure_type == "Cubique Centré (CC)":
        fig.add_trace(go.Scatter3d(
            x=[0.5], y=[0.5], z=[0.5],
            mode='markers',
            marker=dict(size=35, color='#636EFA', opacity=0.9),
            name="Centre (propre à 1 maille)",
            hovertemplate="Centre du cube<extra></extra>"
        ))
        
    elif structure_type == "Cubique à Faces Centrées (CFC)":
        face_x = [0.5, 0.5, 0.5, 0.5, 0, 1]
        face_y = [0.5, 0.5, 0, 1, 0.5, 0.5]
        face_z = [0, 1, 0.5, 0.5, 0.5, 0.5]
        fig.add_trace(go.Scatter3d(
            x=face_x, y=face_y, z=face_z,
            mode='markers',
            marker=dict(size=35, color='#00CC96', opacity=0.9),
            name="Centres des faces (partagés en 2)",
            hovertemplate="Centre de face<extra></extra>"
        ))

    # Mise en forme de la scène 3D
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-0.2, 1.2], visible=False),
            yaxis=dict(range=[-0.2, 1.2], visible=False),
            zaxis=dict(range=[-0.2, 1.2], visible=False),
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        legend=dict(yanchor="top", y=0.95, xanchor="left", x=0.05, bgcolor="rgba(255, 255, 255, 0.8)")
    )
    return fig

# Interface utilisateur Streamlit
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Paramètres")
    choix_maille = st.radio(
        "Sélectionnez la structure cristalline :",
        ["Cubique Simple (CS)", "Cubique Centré (CC)", "Cubique à Faces Centrées (CFC)"]
    )
    
    st.subheader("2. Bilan des atomes (Multiplicité)")
    st.markdown("**Règle de partage :**")
    st.markdown("- 🔴 **Sommet** : appartient à 8 mailles contiguës. Compte pour **1/8**.")
    st.markdown("- 🟢 **Face** : appartient à 2 mailles contiguës. Compte pour **1/2**.")
    st.markdown("- 🔵 **Centre** : appartient uniquement à cette maille. Compte pour **1**.")
    
    st.markdown("---")
    if choix_maille == "Cubique Simple (CS)":
        st.latex(r"Z = 8 \times \frac{1}{8} = 1 \text{ atome/maille}")
    elif choix_maille == "Cubique Centré (CC)":
        st.latex(r"Z = \left(8 \times \frac{1}{8}\right) + \left(1 \times 1\right) = 2 \text{ atomes/maille}")
    elif choix_maille == "Cubique à Faces Centrées (CFC)":
        st.latex(r"Z = \left(8 \times \frac{1}{8}\right) + \left(6 \times \frac{1}{2}\right) = 4 \text{ atomes/maille}")

with col2:
    # Affichage du graphique 3D interactif
    st.plotly_chart(plot_structure(choix_maille), use_container_width=True)
    st.caption("💡 Astuce : Vous pouvez zoomer avec la molette et cliquer-glisser pour tourner la maille dans toutes les directions.")
