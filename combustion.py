import streamlit as st

st.title("🔥 Combustion des Alcanes")
st.write("Idéal pour le cycle 4 : sélectionne le nombre de carbones pour obtenir la formule de l'alcane et équilibrer son équation de combustion complète.")

# Sélection du nombre d'atomes de carbone (n)
n = st.slider("Nombre d'atomes de carbone (n)", min_value=1, max_value=20, value=1)

# Calcul du nombre d'atomes d'hydrogène (2n + 2)
h = 2 * n + 2

# Formatage de la formule brute (gestion du cas n=1 où on omet le "1" pour C)
alcane_formula = f"C_{{{n}}}H_{{{h}}}" if n > 1 else f"CH_{{{h}}}"

st.subheader("Formule brute de l'alcane :")
st.latex(alcane_formula)

# Bouton d'action
if st.button("Résoudre l'équation de combustion"):
    # Logique d'équilibrage : C_nH_2n+2 + O_2 -> CO_2 + H_2O
    # L'oxygène nécessaire du côté droit est : 2*n (pour CO2) + (n+1) (pour H2O) = 3n + 1
    o_atoms = 3 * n + 1
    
    # Au collège, on évite les fractions (ex: 7/2 O2). Si 3n+1 est impair, on double tous les coefficients.
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
        
    # Fonction pour masquer le coefficient "1" (on n'écrit pas 1CO2)
    def fmt_c(coeff):
        return "" if coeff == 1 else str(coeff)

    # Création de la chaîne au format LaTeX
    equation = f"{fmt_c(a)}{alcane_formula} + {fmt_c(b)}O_2 \\rightarrow {fmt_c(c)}CO_2 + {fmt_c(d)}H_2O"
    
    st.subheader("Équation de combustion complète :")
    st.latex(equation)
