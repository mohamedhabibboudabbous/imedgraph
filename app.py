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

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp { background: #0b0f1a; color: #e2e8f0; }

.main-header {
    font-family: 'Space Mono', monospace;
    font-size: 2rem; font-weight: 700; letter-spacing: -1px;
    color: #7dd3fc; border-bottom: 2px solid #1e3a5f;
    padding-bottom: 0.5rem; margin-bottom: 0.25rem;
}
.sub-header {
    font-family: 'DM Sans', sans-serif; font-weight: 300;
    color: #64748b; font-size: 0.95rem; margin-bottom: 2rem;
}
.section-title {
    font-family: 'Space Mono', monospace; font-size: 0.75rem;
    letter-spacing: 3px; text-transform: uppercase;
    color: #38bdf8; margin-bottom: 1rem;
}
.result-card {
    border-radius: 12px; padding: 1.25rem 1.5rem; margin: 0.75rem 0;
    font-family: 'Space Mono', monospace; font-size: 0.9rem; border-left: 4px solid;
}
.card-critical  { background: rgba(239,68,68,0.08);  border-color: #ef4444; color: #fca5a5; }
.card-noncritical { background: rgba(34,197,94,0.08); border-color: #22c55e; color: #86efac; }
.card-info      { background: rgba(56,189,248,0.08); border-color: #38bdf8; color: #7dd3fc; }

.badge { display:inline-block; padding:0.2rem 0.65rem; border-radius:9999px;
         font-family:'Space Mono',monospace; font-size:0.75rem; font-weight:700; letter-spacing:1px; }
.badge-decomp   { background:#ef4444; color:#fff; }
.badge-indecomp { background:#22c55e; color:#0b0f1a; }

.stButton > button {
    background: linear-gradient(135deg,#0ea5e9,#6366f1) !important;
    color:#fff !important; border:none !important; border-radius:8px !important;
    font-family:'Space Mono',monospace !important; font-weight:700 !important;
    letter-spacing:1px !important; padding:0.5rem 1.5rem !important;
    transition:opacity 0.2s ease !important;
}
.stButton > button:hover { opacity:0.85 !important; }

.stTabs [data-baseweb="tab"] {
    font-family:'Space Mono',monospace; font-size:0.8rem; letter-spacing:1px; color:#64748b;
}
.stTabs [aria-selected="true"] { color:#38bdf8 !important; border-bottom-color:#38bdf8 !important; }

hr { border-color:#1e3a5f; margin:1.5rem 0; }

.pairs-table { display:flex; flex-wrap:wrap; gap:0.5rem; margin-top:0.75rem; }
.pair-chip { font-family:'Space Mono',monospace; font-size:0.8rem; padding:0.3rem 0.75rem; border-radius:6px; }
.pair-chip-crit { background:rgba(239,68,68,0.15); color:#fca5a5; border:1px solid #ef4444; }
.pair-chip-ok   { background:rgba(34,197,94,0.12); color:#86efac; border:1px solid #22c55e; }

.row-label {
    font-family:'Space Mono',monospace; font-size:0.85rem; color:#38bdf8;
    padding-top:0.55rem; text-align:right; padding-right:0.75rem;
}
.stTextInput > div > div > input {
    background:#131929 !important; border:1px solid #1e3a5f !important;
    color:#e2e8f0 !important; font-family:'Space Mono',monospace !important;
    border-radius:8px !important; font-size:0.9rem !important;
}
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

def afficher_intervalles_st(mat, label="", sommets_originaux=None):
    """
    sommets_originaux : liste des indices originaux (1-based) des sommets restants.
    Si None, on suppose qu'aucun sommet n'a été supprimé (indices 1..n).
    """
    intervalles = trouver_intervalles(mat)
    n = len(mat)
    if sommets_originaux is None:
        sommets_originaux = list(range(1, n + 1))

    if intervalles:
        chips = "".join(
            f'<span class="pair-chip" style="background:rgba(251,191,36,0.12);color:#fde68a;border:1px solid #f59e0b;">'
            f'{{{", ".join(str(sommets_originaux[x]) for x in iv)}}}</span>'
            for iv in intervalles
        )
        header = f"Intervalles{(' de ' + label) if label else ''} ({len(intervalles)})"
        st.markdown(
            f'<div class="section-title" style="color:#f59e0b;margin-top:1.2rem;">{header}</div>'
            f'<div class="pairs-table">{chips}</div>',
            unsafe_allow_html=True
        )

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
if "page" not in st.session_state:
    st.session_state.page = "saisie"
if "matrix" not in st.session_state:
    st.session_state.matrix = None
if "n" not in st.session_state:
    st.session_state.n = 4


# ══════════════════════════════════════════════════════════════════
#  PAGE 1 — SAISIE DE LA MATRICE
# ══════════════════════════════════════════════════════════════════
if st.session_state.page == "saisie":

    st.markdown('<div class="main-header">🔷 Saisie de la Matrice</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Définissez votre graphe avant de lancer l\'analyse</div>', unsafe_allow_html=True)

    col_n, _ = st.columns([1, 3])
    with col_n:
        n = st.number_input("Nombre de sommets n", min_value=2, max_value=50,
                            value=st.session_state.n, step=1)
        st.session_state.n = n

    st.markdown("---")
    st.markdown(f'<div class="section-title">Matrice {n} × {n}</div>', unsafe_allow_html=True)
    st.caption(f"Entrez {n} valeurs (0 ou 1) séparées par des espaces pour chaque ligne.")

    matrix_input = []
    errors = []

    for i in range(n):
        default_row = " ".join(["0" if i == j else "1" for j in range(n)])
        col_label, col_input = st.columns([0.06, 0.94])
        with col_label:
            st.markdown(f'<div class="row-label">L{i+1}</div>', unsafe_allow_html=True)
        with col_input:
            raw = st.text_input(
                label=f"ligne_{i+1}",
                value=default_row,
                key=f"row_{i}",
                label_visibility="collapsed",
                placeholder=f"{n} valeurs séparées par espaces"
            )
        vals = raw.strip().split()
        if len(vals) != n:
            errors.append(f"Ligne {i+1} : attendu {n} valeurs, reçu {len(vals)}")
        else:
            try:
                row = [int(v) for v in vals]
                if any(v not in (0, 1) for v in row):
                    errors.append(f"Ligne {i+1} : valeurs doivent être 0 ou 1")
                else:
                    matrix_input.append(row)
            except ValueError:
                errors.append(f"Ligne {i+1} : valeurs non entières")

    st.markdown("---")

    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        if st.button("✦ Valider et Analyser →", use_container_width=True):
            if errors:
                for e in errors:
                    st.error(e)
            elif len(matrix_input) != n:
                st.error("Certaines lignes sont incomplètes.")
            else:
                st.session_state.matrix = matrix_input
                st.session_state.page = "analyse"
                st.rerun()

    with col_info:
        if errors:
            st.markdown(f'<div class="result-card card-critical">⚠ {len(errors)} erreur(s) à corriger avant de continuer.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-card card-info">✓ Matrice valide — prête à être analysée.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  PAGE 2 — ANALYSE
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "analyse":

    mat = st.session_state.matrix
    n   = len(mat)

    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Modifier la matrice"):
            st.session_state.page = "saisie"
            st.rerun()
    with col_title:
        st.markdown('<div class="main-header">🔷 Analyse de Décomposition</div>', unsafe_allow_html=True)

    st.markdown('<div class="sub-header">Graphes — Intervalles & Criticalité</div>', unsafe_allow_html=True)

    with st.expander(f"📋 Matrice {n}×{n} — cliquer pour afficher", expanded=False):
        header = "| v |" + "".join(f" {i+1} |" for i in range(n))
        sep    = "|---|" + "---|" * n
        rows   = "\n".join(f"| **{i+1}** |" + "".join(f" {mat[i][j]} |" for j in range(n)) for i in range(n))
        st.markdown(header + "\n" + sep + "\n" + rows)

    indecomp_global = est_indecomposable(mat)
    if indecomp_global:
        st.markdown('<span class="badge badge-indecomp">INDECOMPOSABLE</span>&nbsp; Le graphe initial est indecomposable.', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-decomp">DECOMPOSABLE</span>&nbsp; Le graphe initial est décomposable.', unsafe_allow_html=True)
        afficher_intervalles_st(mat, "G")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "SOMMET UNIQUE", "PAIRE DE SOMMETS", "TOUS LES SOMMETS", "TOUTES LES PAIRES"
    ])

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
                    st.markdown(f'<div class="result-card card-noncritical">Après suppression du sommet <strong>{s}</strong> : INDECOMPOSABLE<br>➜ Sommet <strong>NON critique</strong></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-card card-critical">Après suppression du sommet <strong>{s}</strong> : DECOMPOSABLE<br>➜ Sommet <strong>CRITIQUE</strong></div>', unsafe_allow_html=True)
                    restants = [v for v in range(1, n+1) if v != s]
                    afficher_intervalles_st(mat2, f"G\\{s}", sommets_originaux=restants)

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
                        st.markdown(f'<div class="result-card card-noncritical">Après suppression de <strong>({s1},{s2})</strong> : INDECOMPOSABLE<br>➜ Paire <strong>NON critique</strong></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="result-card card-critical">Après suppression de <strong>({s1},{s2})</strong> : DECOMPOSABLE<br>➜ Paire <strong>CRITIQUE</strong></div>', unsafe_allow_html=True)
                        restants = [v for v in range(1, n+1) if v not in (s1, s2)]
                        afficher_intervalles_st(mat2, f"G\\{{{s1},{s2}}}", sommets_originaux=restants)

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
            # Show intervals for each critical vertex
            if critiques_s:
                st.markdown("---")
                st.markdown('<div class="section-title" style="color:#f59e0b;">Détail des intervalles par sommet critique</div>', unsafe_allow_html=True)
                for s in critiques_s:
                    mat2 = supprimer_sommets(mat, (s,))
                    restants = [v for v in range(1, n+1) if v != s]
                    with st.expander(f"Intervalles de G \\ {{v{s}}}"):
                        afficher_intervalles_st(mat2, sommets_originaux=restants)

    with tab4:
        st.markdown('<div class="section-title">Analyse exhaustive des paires</div>', unsafe_allow_html=True)
        if n < 3:
            st.warning("Il faut au moins 3 sommets pour analyser des paires.")
        elif st.button("Lancer l'analyse complète des paires", key="btn_all"):
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
            # Show intervals for each critical pair
            if critiques:
                st.markdown("---")
                st.markdown('<div class="section-title" style="color:#f59e0b;">Détail des intervalles par paire critique</div>', unsafe_allow_html=True)
                for a, b in critiques:
                    mat2 = supprimer_sommets(mat, (a, b))
                    restants = [v for v in range(1, n+1) if v not in (a, b)]
                    with st.expander(f"Intervalles de G \\ {{v{a}, v{b}}}"):
                        afficher_intervalles_st(mat2, sommets_originaux=restants)