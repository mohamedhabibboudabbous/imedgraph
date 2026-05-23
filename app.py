import streamlit as st
from itertools import combinations

# ─────────────────────────── PAGE CONFIG ───────────────────────────
st.set_page_config(
    page_title="Boudabbous — Testeur de Décomposabilité",
    page_icon="🔷",
    layout="wide",
)

# ─────────────────────────── CUSTOM CSS ────────────────────────────
# Styles inchangés par rapport à la v0 (avec petits ajouts pour le sélecteur de mode)
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
.card-critical    { background: rgba(239,68,68,0.08);  border-color: #ef4444; color: #fca5a5; }
.card-noncritical { background: rgba(34,197,94,0.08);  border-color: #22c55e; color: #86efac; }
.card-info        { background: rgba(56,189,248,0.08); border-color: #38bdf8; color: #7dd3fc; }

.badge { display:inline-block; padding:0.2rem 0.65rem; border-radius:9999px;
         font-family:'Space Mono',monospace; font-size:0.75rem; font-weight:700; letter-spacing:1px; }
.badge-decomp   { background:#ef4444; color:#fff; }
.badge-indecomp { background:#22c55e; color:#0b0f1a; }
.badge-mode     { background:#1e3a5f; color:#7dd3fc; border:1px solid #38bdf8; }

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

/* ── MODE SELECTOR (radio buttons) ── */
.stRadio > label { 
    font-family:'Space Mono',monospace !important; 
    font-size:0.75rem !important; letter-spacing:2px !important; 
    text-transform:uppercase; color:#38bdf8 !important;
}
.stRadio [role="radiogroup"] { gap: 1rem; }

/* ── WELCOME SCREEN ── */
.welcome-overlay {
    position: fixed; inset: 0; z-index: 9999;
    background: #0b0f1a;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center;
    animation: fadeOut 10s ease 1s forwards;
    pointer-events: none;
}
.welcome-title {
    font-family: 'Space Mono', monospace;
    font-size: clamp(1.4rem, 4vw, 2.5rem);
    font-weight: 700;
    color: #7dd3fc;
    letter-spacing: -1px;
    line-height: 1.3;
    max-width: 700px;
    padding: 0 2rem;
    margin-bottom: 1rem;
}
.welcome-title span { color: #38bdf8; }
.welcome-sub {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300; font-size: 1rem;
    color: #475569;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.welcome-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #38bdf8;
    margin: 2rem auto 0;
    animation: pulse 1s ease infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
}
@keyframes fadeOut {
    to { opacity: 0; pointer-events: none; }
}

/* ── FLOATING FOOTER ── */
.floating-footer {
    position: fixed;
    bottom: 1.25rem;
    right: 1.5rem;
    z-index: 1000;
    background: rgba(14, 22, 38, 0.85);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid #1e3a5f;
    border-radius: 999px;
    padding: 0.4rem 1.1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #38bdf8;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    white-space: nowrap;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    pointer-events: none;
    user-select: none;
}
.floating-footer span { color: #475569; margin: 0 0.4rem; }

.main > div { padding-bottom: 4rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── WELCOME SCREEN ────────────────────────
st.markdown("""
<div class="welcome-overlay" id="welcomeOverlay">
    <div class="welcome-title">
        Bienvenue à <span>Boudabbous</span><br>
        Testeur de Décomposabilité des Graphes &amp; Tournois
    </div>
    <div class="welcome-sub">Analyse · Intervalles · Criticalité</div>
    <div class="welcome-dot"></div>
</div>
<script>
(function(){
    var el = document.getElementById('welcomeOverlay');
    if (!el) return;
    if (sessionStorage.getItem('welcomed')) {
        el.style.display = 'none';
    } else {
        sessionStorage.setItem('welcomed', '1');
    }
})();
</script>
""", unsafe_allow_html=True)

# ─────────────────────────── FLOATING FOOTER ───────────────────────
st.markdown("""
<div class="floating-footer">
    🔷<span>·</span>Boudabbous<span>·</span>Graphes &amp; Tournois
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  CORE LOGIC — version généralisée (Graphe OU Tournoi)
# ════════════════════════════════════════════════════════════════════
#
# Définition d'un INTERVALLE (commune aux deux modes) :
#   Un sous-ensemble S de sommets est un intervalle si tous les sommets
#   de S "se comportent pareillement" vis-à-vis de chaque sommet x ∉ S.
#
#   - GRAPHE non orienté : mat[x][u] = mat[x][u0]  (et symétrique)
#     → tous les u ∈ S sont voisins ou non-voisins de x de la même façon.
#
#   - TOURNOI (graphe orienté complet) : mat[x][u] = mat[x][u0]
#                                        ET mat[u][x] = mat[u0][x]
#     → tous les u ∈ S ont le même SENS d'arête avec x
#       (x→u pour tous, ou u→x pour tous).
#
# En pratique, la condition `mat[x][u] != mat[x][u0] or mat[u][x] != mat[u0][x]`
# fonctionne pour les DEUX modes : dans le cas non orienté la matrice est
# symétrique donc la 2ème condition est redondante mais inoffensive.
# C'est pour cela qu'on peut garder UNE seule fonction `est_intervalle`.
# ════════════════════════════════════════════════════════════════════

def est_intervalle(mat, subset):
    """Vérifie si `subset` est un intervalle de la matrice `mat`.
    Fonctionne aussi bien pour les graphes que pour les tournois."""
    S = set(subset)
    outside = [x for x in range(len(mat)) if x not in S]
    u0 = subset[0]  # sommet de référence dans S
    for x in outside:
        for u in subset[1:]:
            # Pour un tournoi : il faut vérifier le sens dans les DEUX directions.
            # Pour un graphe : la matrice est symétrique donc c'est équivalent.
            if mat[x][u] != mat[x][u0] or mat[u][x] != mat[u0][x]:
                return False
    return True

def trouver_intervalles(mat):
    """Retourne tous les intervalles non triviaux (taille 2 à n-1)."""
    n = len(mat)
    res = []
    for k in range(2, n):
        for comb in combinations(range(n), k):
            if est_intervalle(mat, comb):
                res.append(comb)
    return res

def est_indecomposable(mat):
    """Un graphe/tournoi est indécomposable s'il n'a aucun intervalle non trivial."""
    return len(trouver_intervalles(mat)) == 0

def afficher_intervalles_st(mat, label="", sommets_originaux=None):
    """Affichage stylisé des intervalles trouvés."""
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
    """Retourne une sous-matrice sans les sommets indiqués (numérotés à partir de 1)."""
    indices = {s - 1 for s in sommets}
    return [
        [val for j, val in enumerate(ligne) if j not in indices]
        for i, ligne in enumerate(mat)
        if i not in indices
    ]

def analyser_tous_sommets(mat):
    """Pour chaque sommet : critique si sa suppression rend le graphe décomposable."""
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
    """Idem mais pour toutes les paires de sommets."""
    n = len(mat)
    critiques, non_critiques = [], []
    for s1, s2 in combinations(range(1, n + 1), 2):
        mat2 = supprimer_sommets(mat, (s1, s2))
        if est_indecomposable(mat2):
            non_critiques.append((s1, s2))
        else:
            critiques.append((s1, s2))
    return critiques, non_critiques


# ════════════════════════════════════════════════════════════════════
#  VALIDATION DES MATRICES (différente selon le mode)
# ════════════════════════════════════════════════════════════════════

def valider_matrice_graphe(mat, n):
    """
    Pour un GRAPHE non orienté :
      - valeurs ∈ {0, 1}
      - diagonale = 0
      - matrice symétrique : mat[i][j] = mat[j][i]
    Retourne une liste d'erreurs (vide si OK).
    """
    errors = []
    for i in range(n):
        for j in range(n):
            v = mat[i][j]
            if v not in (0, 1):
                errors.append(f"Cellule ({i+1},{j+1}) : valeur {v} invalide (doit être 0 ou 1)")
        if mat[i][i] != 0:
            errors.append(f"Diagonale : mat[{i+1}][{i+1}] doit être 0")
    for i in range(n):
        for j in range(i+1, n):
            if mat[i][j] != mat[j][i]:
                errors.append(f"Non symétrique : mat[{i+1}][{j+1}]={mat[i][j]} ≠ mat[{j+1}][{i+1}]={mat[j][i]}")
    return errors

def valider_matrice_tournoi(mat, n):
    """
    Pour un TOURNOI :
      - valeurs ∈ {-1, 0, 1}
      - diagonale = 0
      - antisymétrique : mat[i][j] = -mat[j][i] (pour i ≠ j)
      - chaque arête existe : mat[i][j] ∈ {-1, +1} pour i ≠ j (pas de 0 hors diagonale)
    """
    errors = []
    for i in range(n):
        for j in range(n):
            v = mat[i][j]
            if i == j:
                if v != 0:
                    errors.append(f"Diagonale : mat[{i+1}][{i+1}] doit être 0 (reçu {v})")
            else:
                if v not in (-1, 1):
                    errors.append(f"Cellule ({i+1},{j+1}) : valeur {v} invalide (doit être -1 ou 1 hors diagonale)")
    for i in range(n):
        for j in range(i+1, n):
            if mat[i][j] + mat[j][i] != 0:
                errors.append(f"Non antisymétrique : mat[{i+1}][{j+1}]={mat[i][j]} et mat[{j+1}][{i+1}]={mat[j][i]} (doivent être opposés)")
    return errors


# ─────────────────────────── SESSION STATE ─────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "saisie"
if "matrix" not in st.session_state:
    st.session_state.matrix = None
if "n" not in st.session_state:
    st.session_state.n = 4
if "mode" not in st.session_state:
    st.session_state.mode = "Graphe"   # "Graphe" ou "Tournoi"


# ══════════════════════════════════════════════════════════════════
#  PAGE 1 — SAISIE DE LA MATRICE
# ══════════════════════════════════════════════════════════════════
if st.session_state.page == "saisie":

    st.markdown('<div class="main-header">🔷 Boudabbous — Saisie de la Matrice</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Définissez votre structure avant de lancer l\'analyse</div>', unsafe_allow_html=True)

    # ── Sélection du MODE (Graphe ou Tournoi) ──
    col_mode, col_n, _ = st.columns([2, 1, 2])
    with col_mode:
        mode = st.radio(
            "Type de structure",
            options=["Graphe", "Tournoi"],
            horizontal=True,
            index=0 if st.session_state.mode == "Graphe" else 1,
            help="Graphe = non orienté (0/1 symétrique) · Tournoi = orienté complet (±1 antisymétrique)"
        )
        st.session_state.mode = mode
    with col_n:
        n = st.number_input("Nombre de sommets n", min_value=2, max_value=50,
                            value=st.session_state.n, step=1)
        st.session_state.n = n

    # ── Encart explicatif selon le mode ──
    if mode == "Graphe":
        st.markdown(
            '<div class="result-card card-info">'
            '<strong>Mode GRAPHE non orienté</strong> — Valeurs <code>0</code> ou <code>1</code>. '
            'La matrice doit être <strong>symétrique</strong> avec une diagonale nulle.<br>'
            '<code>mat[i][j] = 1</code> ⇔ arête entre i et j.'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="result-card card-info">'
            '<strong>Mode TOURNOI</strong> — Valeurs <code>-1</code> ou <code>1</code> hors diagonale, '
            '<code>0</code> sur la diagonale. La matrice doit être <strong>antisymétrique</strong>.<br>'
            '<code>mat[a][b] = 1</code> ⇔ arête orientée a → b · <code>mat[a][b] = -1</code> ⇔ arête orientée b → a.'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown(f'<div class="section-title">Matrice {n} × {n} — Mode {mode}</div>', unsafe_allow_html=True)

    # Indication pour la saisie selon le mode
    if mode == "Graphe":
        st.caption(f"Entrez {n} valeurs (0 ou 1) séparées par des espaces pour chaque ligne. "
                   f"La diagonale doit valoir 0 et la matrice doit être symétrique.")
    else:
        st.caption(f"Entrez {n} valeurs (-1, 0 ou 1) séparées par des espaces pour chaque ligne. "
                   f"La diagonale vaut 0 ; hors diagonale : -1 ou 1 (antisymétrique).")

    matrix_input = []
    parse_errors = []

    # ── Génération dynamique des valeurs par défaut selon le mode ──
    for i in range(n):
        if mode == "Graphe":
            # Graphe complet par défaut (sauf diagonale)
            default_row = " ".join(["0" if i == j else "1" for j in range(n)])
        else:
            # Tournoi par défaut : a→b si a<b (1 au-dessus de la diag, -1 en dessous)
            default_row = " ".join([
                "0" if i == j else ("1" if i < j else "-1")
                for j in range(n)
            ])

        col_label, col_input = st.columns([0.06, 0.94])
        with col_label:
            st.markdown(f'<div class="row-label">L{i+1}</div>', unsafe_allow_html=True)
        with col_input:
            raw = st.text_input(
                label=f"ligne_{i+1}",
                value=default_row,
                key=f"row_{i}_{mode}",   # clé inclut le mode pour réinitialiser au changement
                label_visibility="collapsed",
                placeholder=f"{n} valeurs séparées par espaces"
            )
        vals = raw.strip().split()
        if len(vals) != n:
            parse_errors.append(f"Ligne {i+1} : attendu {n} valeurs, reçu {len(vals)}")
        else:
            try:
                row = [int(v) for v in vals]
                matrix_input.append(row)
            except ValueError:
                parse_errors.append(f"Ligne {i+1} : valeurs non entières")

    # ── Validation selon le mode (uniquement si parsing OK) ──
    structural_errors = []
    if not parse_errors and len(matrix_input) == n:
        if mode == "Graphe":
            structural_errors = valider_matrice_graphe(matrix_input, n)
        else:
            structural_errors = valider_matrice_tournoi(matrix_input, n)

    all_errors = parse_errors + structural_errors

    st.markdown("---")

    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        if st.button("✦ Valider et Analyser →", use_container_width=True):
            if all_errors:
                for e in all_errors:
                    st.error(e)
            elif len(matrix_input) != n:
                st.error("Certaines lignes sont incomplètes.")
            else:
                st.session_state.matrix = matrix_input
                st.session_state.page = "analyse"
                st.rerun()

    with col_info:
        if all_errors:
            st.markdown(
                f'<div class="result-card card-critical">⚠ {len(all_errors)} erreur(s) à corriger avant de continuer.</div>',
                unsafe_allow_html=True
            )
            # Afficher les premières erreurs pour aider l'utilisateur
            with st.expander("Voir les erreurs"):
                for e in all_errors[:20]:
                    st.markdown(f"- {e}")
                if len(all_errors) > 20:
                    st.markdown(f"... et {len(all_errors) - 20} autres erreurs.")
        else:
            st.markdown(
                f'<div class="result-card card-info">✓ Matrice {mode.lower()} valide — prête à être analysée.</div>',
                unsafe_allow_html=True
            )


# ══════════════════════════════════════════════════════════════════
#  PAGE 2 — ANALYSE
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "analyse":

    mat  = st.session_state.matrix
    n    = len(mat)
    mode = st.session_state.mode

    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Modifier la matrice"):
            st.session_state.page = "saisie"
            st.rerun()
    with col_title:
        st.markdown('<div class="main-header">🔷 Boudabbous — Analyse de Décomposition</div>', unsafe_allow_html=True)

    # Affichage du badge MODE en cours
    st.markdown(
        f'<div class="sub-header">'
        f'<span class="badge badge-mode">MODE : {mode.upper()}</span>'
        f'&nbsp;&nbsp; Intervalles &amp; Criticalité'
        f'</div>',
        unsafe_allow_html=True
    )

    # ── Affichage de la matrice (en markdown) ──
    with st.expander(f"📋 Matrice {n}×{n} ({mode}) — cliquer pour afficher", expanded=False):
        header = "| v |" + "".join(f" {i+1} |" for i in range(n))
        sep    = "|---|" + "---|" * n
        rows   = "\n".join(
            f"| **{i+1}** |" + "".join(f" {mat[i][j]} |" for j in range(n))
            for i in range(n)
        )
        st.markdown(header + "\n" + sep + "\n" + rows)

    # ── Décomposabilité globale ──
    indecomp_global = est_indecomposable(mat)
    nom_structure = "tournoi" if mode == "Tournoi" else "graphe"
    if indecomp_global:
        st.markdown(
            f'<span class="badge badge-indecomp">INDECOMPOSABLE</span>&nbsp; '
            f'Le {nom_structure} initial est indécomposable.',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<span class="badge badge-decomp">DECOMPOSABLE</span>&nbsp; '
            f'Le {nom_structure} initial est décomposable.',
            unsafe_allow_html=True
        )
        label_init = "T" if mode == "Tournoi" else "G"
        afficher_intervalles_st(mat, label_init)

    st.markdown("---")

    # ── Onglets d'analyse ──
    tab1, tab2, tab3, tab4 = st.tabs([
        "SOMMET UNIQUE", "PAIRE DE SOMMETS", "TOUS LES SOMMETS", "TOUTES LES PAIRES"
    ])

    # Lettre utilisée dans les labels selon le mode (G pour graphe, T pour tournoi)
    L = "T" if mode == "Tournoi" else "G"

    # ─── Tab 1 : sommet unique ───
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
                    st.markdown(
                        f'<div class="result-card card-noncritical">Après suppression du sommet '
                        f'<strong>{s}</strong> : INDECOMPOSABLE<br>➜ Sommet <strong>NON critique</strong></div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="result-card card-critical">Après suppression du sommet '
                        f'<strong>{s}</strong> : DECOMPOSABLE<br>➜ Sommet <strong>CRITIQUE</strong></div>',
                        unsafe_allow_html=True
                    )
                    restants = [v for v in range(1, n+1) if v != s]
                    afficher_intervalles_st(mat2, f"{L}\\{s}", sommets_originaux=restants)

    # ─── Tab 2 : paire de sommets ───
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
                        st.markdown(
                            f'<div class="result-card card-noncritical">Après suppression de '
                            f'<strong>({s1},{s2})</strong> : INDECOMPOSABLE<br>'
                            f'➜ Paire <strong>NON critique</strong></div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="result-card card-critical">Après suppression de '
                            f'<strong>({s1},{s2})</strong> : DECOMPOSABLE<br>'
                            f'➜ Paire <strong>CRITIQUE</strong></div>',
                            unsafe_allow_html=True
                        )
                        restants = [v for v in range(1, n+1) if v not in (s1, s2)]
                        afficher_intervalles_st(mat2, f"{L}\\{{{s1},{s2}}}", sommets_originaux=restants)

    # ─── Tab 3 : tous les sommets ───
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
                    st.markdown('<div class="result-card card-noncritical">Aucun sommet critique</div>',
                                unsafe_allow_html=True)
            with col_b:
                st.markdown(f"**Sommets non critiques** ({len(non_critiques_s)})")
                if non_critiques_s:
                    chips = "".join(f'<span class="pair-chip pair-chip-ok">v{s}</span>' for s in non_critiques_s)
                    st.markdown(f'<div class="pairs-table">{chips}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="result-card card-critical">Aucun sommet non critique</div>',
                                unsafe_allow_html=True)
            if critiques_s:
                st.markdown("---")
                st.markdown('<div class="section-title" style="color:#f59e0b;">Détail des intervalles par sommet critique</div>',
                            unsafe_allow_html=True)
                for s in critiques_s:
                    mat2 = supprimer_sommets(mat, (s,))
                    restants = [v for v in range(1, n+1) if v != s]
                    with st.expander(f"Intervalles de {L} \\ {{v{s}}}"):
                        afficher_intervalles_st(mat2, sommets_originaux=restants)

    # ─── Tab 4 : toutes les paires ───
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
                    st.markdown('<div class="result-card card-noncritical">Aucune paire critique</div>',
                                unsafe_allow_html=True)
            with col_b:
                st.markdown(f"**Paires non critiques** ({len(non_critiques)})")
                if non_critiques:
                    chips = "".join(f'<span class="pair-chip pair-chip-ok">({a},{b})</span>' for a, b in non_critiques)
                    st.markdown(f'<div class="pairs-table">{chips}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="result-card card-critical">Aucune paire non critique</div>',
                                unsafe_allow_html=True)
            if critiques:
                st.markdown("---")
                st.markdown('<div class="section-title" style="color:#f59e0b;">Détail des intervalles par paire critique</div>',
                            unsafe_allow_html=True)
                for a, b in critiques:
                    mat2 = supprimer_sommets(mat, (a, b))
                    restants = [v for v in range(1, n+1) if v not in (a, b)]
                    with st.expander(f"Intervalles de {L} \\ {{v{a}, v{b}}}"):
                        afficher_intervalles_st(mat2, sommets_originaux=restants)