import streamlit as st

st.title("🔥 Combustion des Alcanes")
st.write("Idéal pour le cycle 4 : sélectionne le nombre de carbones pour obtenir la formule de l'alcane et équilibrer son équation de combustion complète.")

# Sélection du nombre d'atomes de carbone (n)
n = st.slider("Nombre d'atomes de carbone (n)", min_value=1, max_value=20, value=1)

# Calcul du nombre d'atomes d'hydrogène (2n + 2)
h = 2 * n + 2

# Formatage de la formule brute
alcane_formula = f"C_{{{n}}}H_{{{h}}}" if n > 1 else f"CH_{{{h}}}"

st.subheader("Formule brute de l'alcane :")
# On ajoute l'indice (g) à l'affichage de la formule brute
st.latex(f"{{{alcane_formula}}}_{{(g)}}")

# Bouton d'action
if st.button("Résoudre l'équation de combustion"):
    # Logique d'équilibrage : C_nH_2n+2 + O_2 -> CO_2 + H_2O
    o_atoms = 3 * n + 1
    
    if o_atoms % 2 == 0:
        a = 1
        b = o_atoms // 2
        c = n
        d = n + 1
    else:
        a = 2
        b = o_atoms
        c = 2 * n
        d = 2 * (n + 1)
        
    def fmt_c(coeff):
        return "" if coeff == 1 else str(coeff)

    # Création de la chaîne au format LaTeX
    # 1. \xrightarrow{\text{énergie}} crée la flèche avec le mot au-dessus
    # 2. Les molécules sont mises entre accolades {...}_{(g)} pour grouper correctement l'indice
    equation = (
        f"{fmt_c(a)}{{{alcane_formula}}}_{{(g)}} + "
        f"{fmt_c(b)}{{O_2}}_{{(g)}} "
        f"\\xrightarrow{{\\text{{énergie}}}} "
        f"{fmt_c(c)}{{CO_2}}_{{(g)}} + "
        f"{fmt_c(d)}{{H_2O}}_{{(g)}}"
    )
    
    st.subheader("Équation de combustion complète :")
    st.latex(equation)
