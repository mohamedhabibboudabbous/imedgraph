import streamlit as st
from itertools import combinations

# ─────────────────────────── PAGE CONFIG ───────────────────────────
st.set_page_config(
    page_title="Analyse de Graphes",
    page_icon="🔷",
    layout="wide",
)

# ─────────────────────────── CUSTOM CSS ────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: #0b0f1a;
    color: #e2e8f0;
}

/* Header */
.main-header {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -1px;
    color: #7dd3fc;
    border-bottom: 2px solid #1e3a5f;
    padding-bottom: 0.5rem;
    margin-bottom: 0.25rem;
}
.sub-header {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    color: #64748b;
    font-size: 0.95rem;
    margin-bottom: 2rem;
}

/* Section titles */
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 1rem;
}

/* Cards */
.result-card {
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin: 0.75rem 0;
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    border-left: 4px solid;
}
.card-critical {
    background: rgba(239, 68, 68, 0.08);
    border-color: #ef4444;
    color: #fca5a5;
}
.card-noncritical {
    background: rgba(34, 197, 94, 0.08);
    border-color: #22c55e;
    color: #86efac;
}
.card-info {
    background: rgba(56, 189, 248, 0.08);
    border-color: #38bdf8;
    color: #7dd3fc;
}

/* Badge */
.badge {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 9999px;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
}
.badge-decomp { background: #ef4444; color: #fff; }
.badge-indecomp { background: #22c55e; color: #0b0f1a; }

/* Inputs */
.stNumberInput input, .stTextInput input {
    background: #131929 !important;
    border: 1px solid #1e3a5f !important;
    color: #e2e8f0 !important;
    font-family: 'Space Mono', monospace !important;
    border-radius: 8px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s ease !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 1px;
    color: #64748b;
}
.stTabs [aria-selected="true"] {
    color: #38bdf8 !important;
    border-bottom-color: #38bdf8 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f1623 !important;
    border-right: 1px solid #1e3a5f;
}

/* Matrix cell inputs */
.matrix-grid input {
    text-align: center;
    width: 3rem !important;
}

/* Divider */
hr {
    border-color: #1e3a5f;
    margin: 1.5rem 0;
}

/* Pairs table */
.pairs-table {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.75rem;
}
.pair-chip {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    padding: 0.3rem 0.75rem;
    border-radius: 6px;
}
.pair-chip-crit { background: rgba(239,68,68,0.15); color: #fca5a5; border: 1px solid #ef4444; }
.pair-chip-ok   { background: rgba(34,197,94,0.12); color: #86efac; border: 1px solid #22c55e; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────── CORE LOGIC ────────────────────────────
def est_intervalle(mat, subset):
    S = set(subset)
    outside = [x for x in range(len(mat)) if x not in S]
    u0 = subset[0]
    for x in outside:
        for u in subset[1:]:
            if mat[x][u] != mat[x][u0] or mat[u][x] != mat[u0][x]:
                return False
    return True


def trouver_intervalles(mat):
    n = len(mat)
    res = []
    for k in range(2, n):
        for comb in combinations(range(n), k):
            if est_intervalle(mat, comb):
                res.append(comb)
    return res


def est_indecomposable(mat):
    return len(trouver_intervalles(mat)) == 0


def supprimer_sommets(mat, sommets):
    indices = {s - 1 for s in sommets}
    return [
        [val for j, val in enumerate(ligne) if j not in indices]
        for i, ligne in enumerate(mat)
        if i not in indices
    ]


def analyser_tous_sommets(mat):
    n = len(mat)
    critiques, non_critiques = [], []
    for s in range(1, n + 1):
        mat2 = supprimer_sommets(mat, (s,))
        if len(mat2) < 2:
            continue
        if est_indecomposable(mat2):
            non_critiques.append(s)
        else:
            critiques.append(s)
    return critiques, non_critiques


def analyser_toutes_paires(mat):
    n = len(mat)
    critiques, non_critiques = [], []
    for s1, s2 in combinations(range(1, n + 1), 2):
        mat2 = supprimer_sommets(mat, (s1, s2))
        if est_indecomposable(mat2):
            non_critiques.append((s1, s2))
        else:
            critiques.append((s1, s2))
    return critiques, non_critiques


# ─────────────────────────── SESSION STATE ─────────────────────────
if "matrix" not in st.session_state:
    st.session_state.matrix = None
if "n" not in st.session_state:
    st.session_state.n = 4


# ─────────────────────────── SIDEBAR ───────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-title">Paramètres</div>', unsafe_allow_html=True)
    n = st.number_input("Nombre de sommets n", min_value=2, max_value=10,
                        value=st.session_state.n, step=1)
    st.session_state.n = n

    st.markdown("---")
    st.markdown('<div class="section-title">Matrice d\'adjacence</div>', unsafe_allow_html=True)
    st.caption("Entrez les valeurs (0 ou 1) ligne par ligne.")

    matrix_input = []
    for i in range(n):
        row = []
        cols = st.columns(n)
        for j in range(n):
            default = 1 if i != j else 0
            val = cols[j].number_input(
                f"[{i+1},{j+1}]", min_value=0, max_value=1,
                value=default, step=1,
                key=f"cell_{i}_{j}", label_visibility="collapsed"
            )
            row.append(val)
        matrix_input.append(row)

    st.markdown("")
    if st.button("✦ Valider la matrice", use_container_width=True):
        st.session_state.matrix = matrix_input
        st.success("Matrice chargée !")


# ─────────────────────────── MAIN AREA ─────────────────────────────
st.markdown('<div class="main-header">🔷 Analyse de Décomposition</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Graphes — Intervalles & Criticalité</div>', unsafe_allow_html=True)

mat = st.session_state.matrix

if mat is None:
    st.markdown("""
    <div class="result-card card-info">
        ← Configurez votre matrice dans la barre latérale puis cliquez sur <strong>Valider</strong>.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Show current matrix
n = len(mat)
st.markdown('<div class="section-title">Matrice courante</div>', unsafe_allow_html=True)
header = "| v |" + "".join(f" {i+1} |" for i in range(n))
sep    = "|---|" + "---|" * n
rows   = "\n".join(f"| **{i+1}** |" + "".join(f" {mat[i][j]} |" for j in range(n)) for i in range(n))
st.markdown(header + "\n" + sep + "\n" + rows)

st.markdown("---")

# Global decomposability
indecomp_global = est_indecomposable(mat)
if indecomp_global:
    st.markdown('<span class="badge badge-indecomp">INDECOMPOSABLE</span>&nbsp; Le graphe initial est indecomposable.', unsafe_allow_html=True)
else:
    st.markdown('<span class="badge badge-decomp">DECOMPOSABLE</span>&nbsp; Le graphe initial est décomposable.', unsafe_allow_html=True)

st.markdown("---")

# ── Tabs ──
tab1, tab2, tab3, tab4 = st.tabs(["SOMMET UNIQUE", "PAIRE DE SOMMETS", "TOUS LES SOMMETS", "TOUTES LES PAIRES"])

# ── Tab 1: Single vertex ──
with tab1:
    st.markdown('<div class="section-title">Test d\'un sommet</div>', unsafe_allow_html=True)
    s = st.number_input("Sommet à supprimer", min_value=1, max_value=n, value=1, step=1, key="s1")
    if st.button("Analyser le sommet", key="btn_s1"):
        mat2 = supprimer_sommets(mat, (s,))
        if len(mat2) < 2:
            st.warning("Matrice résultante trop petite pour l'analyse.")
        else:
            indecomp = est_indecomposable(mat2)
            if indecomp:
                st.markdown(f"""
                <div class="result-card card-noncritical">
                    Après suppression du sommet <strong>{s}</strong> : graphe INDECOMPOSABLE<br>
                    ➜ Sommet <strong>NON critique</strong>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-card card-critical">
                    Après suppression du sommet <strong>{s}</strong> : graphe DECOMPOSABLE<br>
                    ➜ Sommet <strong>CRITIQUE</strong>
                </div>""", unsafe_allow_html=True)

# ── Tab 2: Pair ──
with tab2:
    st.markdown('<div class="section-title">Test d\'une paire</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        s1 = st.number_input("Sommet 1", min_value=1, max_value=n, value=1, step=1, key="ps1")
    with c2:
        s2 = st.number_input("Sommet 2", min_value=1, max_value=n, value=2, step=1, key="ps2")
    if st.button("Analyser la paire", key="btn_pair"):
        if s1 == s2:
            st.error("Veuillez choisir deux sommets différents.")
        else:
            mat2 = supprimer_sommets(mat, (s1, s2))
            if len(mat2) < 2:
                st.warning("Matrice résultante trop petite pour l'analyse.")
            else:
                indecomp = est_indecomposable(mat2)
                if indecomp:
                    st.markdown(f"""
                    <div class="result-card card-noncritical">
                        Après suppression de la paire <strong>({s1}, {s2})</strong> : graphe INDECOMPOSABLE<br>
                        ➜ Paire <strong>NON critique</strong>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-card card-critical">
                        Après suppression de la paire <strong>({s1}, {s2})</strong> : graphe DECOMPOSABLE<br>
                        ➜ Paire <strong>CRITIQUE</strong>
                    </div>""", unsafe_allow_html=True)

# ── Tab 3: All vertices ──
with tab3:
    st.markdown('<div class="section-title">Analyse de tous les sommets</div>', unsafe_allow_html=True)
    if st.button("Lancer l'analyse de tous les sommets", key="btn_all_s"):
        with st.spinner("Calcul en cours..."):
            critiques_s, non_critiques_s = analyser_tous_sommets(mat)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Sommets critiques** ({len(critiques_s)})")
            if critiques_s:
                chips = "".join(f'<span class="pair-chip pair-chip-crit">v{s}</span>' for s in critiques_s)
                st.markdown(f'<div class="pairs-table">{chips}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="result-card card-noncritical">Aucun sommet critique</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown(f"**Sommets non critiques** ({len(non_critiques_s)})")
            if non_critiques_s:
                chips = "".join(f'<span class="pair-chip pair-chip-ok">v{s}</span>' for s in non_critiques_s)
                st.markdown(f'<div class="pairs-table">{chips}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="result-card card-critical">Aucun sommet non critique</div>', unsafe_allow_html=True)

# ── Tab 4: All pairs ──
with tab4:
    st.markdown('<div class="section-title">Analyse exhaustive</div>', unsafe_allow_html=True)
    if n < 3:
        st.warning("Il faut au moins 3 sommets pour analyser des paires.")
    elif st.button("Lancer l'analyse complète", key="btn_all"):
        with st.spinner("Calcul en cours..."):
            critiques, non_critiques = analyser_toutes_paires(mat)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Paires critiques** ({len(critiques)})")
            if critiques:
                chips = "".join(f'<span class="pair-chip pair-chip-crit">({a},{b})</span>' for a, b in critiques)
                st.markdown(f'<div class="pairs-table">{chips}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="result-card card-noncritical">Aucune paire critique</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown(f"**Paires non critiques** ({len(non_critiques)})")
            if non_critiques:
                chips = "".join(f'<span class="pair-chip pair-chip-ok">({a},{b})</span>' for a, b in non_critiques)
                st.markdown(f'<div class="pairs-table">{chips}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="result-card card-critical">Aucune paire non critique</div>', unsafe_allow_html=True)
