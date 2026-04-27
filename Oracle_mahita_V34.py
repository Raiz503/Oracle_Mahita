"""
╔══════════════════════════════════════════════════════════════╗
║           ORACLE MAHITA V34 — APPLICATION PRINCIPALE        ║
║           Cerveau I intégré (moteur_cerveau1.py)            ║
║           Streamlit · EasyOCR · Pandas · JSON               ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import easyocr
import re
import json
import os
from difflib import get_close_matches
from PIL import Image
import numpy as np

# ── Import du Cerveau I ──────────────────────────────────────
from moteur_cerveau1 import cerveau1 as oracle_brain

# ── Configuration de la page ─────────────────────────────────
st.set_page_config(page_title="Oracle Mahita V34", layout="wide", page_icon="🔮")

# ── STYLE CSS ────────────────────────────────────────────────
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 25px;
        border: 5px solid #7FFFD4;
        border-radius: 20px;
        background-color: #0E1117;
        box-shadow: 0px 0px 30px #7FFFD4;
        margin-bottom: 15px;
    }
    .header-title {
        color: #FFFFFF;
        font-size: 3.5em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 6px;
        margin: 0;
        -webkit-text-stroke: 1.5px #7FFFD4;
        text-shadow: 0px 0px 15px #7FFFD4;
    }
    .header-subtitle {
        color: #7FFFD4;
        font-size: 0.95em;
        margin-top: 8px;
        letter-spacing: 3px;
    }
    .prono-safe    { border-left: 5px solid #00FF00; padding: 12px; background: rgba(0,255,0,0.08);   margin-bottom: 10px; border-radius: 5px; }
    .prono-risque  { border-left: 5px solid #FFA500; padding: 12px; background: rgba(255,165,0,0.08); margin-bottom: 10px; border-radius: 5px; }
    .prono-fun     { border-left: 5px solid #FF4B4B; padding: 12px; background: rgba(255,75,75,0.08);  margin-bottom: 10px; border-radius: 5px; }
    .alerte-oracle { color: #FFD700; font-size: 0.82em; font-style: italic; margin-top: 4px; }
    .alerte-danger { color: #FF4B4B; font-size: 0.82em; font-style: italic; margin-top: 4px; }
    .module-box    { background: rgba(127,255,212,0.05); border: 1px solid #7FFFD4; border-radius: 8px; padding: 10px; margin: 6px 0; }
    .stSelectbox div[data-baseweb="select"] { border-color: #7FFFD4 !important; }
    .next-day-box  { text-align: center; color: #7FFFD4; font-weight: bold; font-size: 1.2em; margin-top: 10px; }
    .indice-banker  { color: #00FF00; font-weight: 900; font-size: 1.1em; }
    .indice-risque  { color: #FFA500; font-weight: 900; font-size: 1.1em; }
    .indice-fun     { color: #FF4B4B; font-weight: 900; font-size: 1.1em; }
    </style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  FONCTIONS UTILITAIRES
# ════════════════════════════════════════════════════════════

def custom_notify(text, color="#00FF00"):
    st.markdown(
        f"""<div style="padding:15px;border:3px solid {color};border-radius:10px;
        background-color:#0E1117;color:#FFFFFF;text-align:center;font-weight:900;
        box-shadow:0px 0px 20px {color};margin:15px 0px;font-size:1.2em;
        text-transform:uppercase;-webkit-text-stroke:1px {color};">{text}</div>""",
        unsafe_allow_html=True
    )


def get_standings(season_data, teams_list):
    """Calcule le classement à partir des résultats enregistrés."""
    stats = {t: {"MJ":0,"V":0,"N":0,"D":0,"BP":0,"BC":0,"Diff":0,"Pts":0} for t in teams_list}
    for jk, data in season_data.items():
        for m in data.get("res", []):
            try:
                s_h, s_a = map(int, m['s'].replace('-', ':').split(':'))
                h, a = m['h'], m['a']
                if h in stats and a in stats:
                    stats[h]["MJ"] += 1; stats[a]["MJ"] += 1
                    stats[h]["BP"] += s_h; stats[h]["BC"] += s_a
                    stats[a]["BP"] += s_a; stats[a]["BC"] += s_h
                    if s_h > s_a:
                        stats[h]["V"] += 1; stats[h]["Pts"] += 3; stats[a]["D"] += 1
                    elif s_h < s_a:
                        stats[a]["V"] += 1; stats[a]["Pts"] += 3; stats[h]["D"] += 1
                    else:
                        stats[h]["N"] += 1; stats[h]["Pts"] += 1
                        stats[a]["N"] += 1; stats[a]["Pts"] += 1
            except:
                continue
    df = pd.DataFrame.from_dict(stats, orient='index').reset_index().rename(columns={'index': 'Équipe'})
    for t in stats:
        df.loc[df['Équipe'] == t, 'Diff'] = stats[t]['BP'] - stats[t]['BC']
    df = df.sort_values(by=["Pts","Diff","BP"], ascending=False).reset_index(drop=True)
    df.insert(0, 'Rang', range(1, len(df)+1))
    return df


def get_forme_equipe(history, saison, equipe, nb_matchs=6):
    """
    Extrait les derniers résultats d'une équipe depuis l'historique JSON.
    Retourne une liste ex: ['V','V','N','D','V'] du plus ancien au plus récent.
    """
    resultats = []
    journees = sorted(
        history[saison].keys(),
        key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0
    )
    for jk in reversed(journees):
        if len(resultats) >= nb_matchs:
            break
        for match in history[saison][jk].get("res", []):
            try:
                sh, sa = map(int, match["s"].replace("-", ":").split(":"))
                if match["h"] == equipe:
                    resultats.insert(0, "V" if sh > sa else ("N" if sh == sa else "D"))
                elif match["a"] == equipe:
                    resultats.insert(0, "V" if sa > sh else ("N" if sh == sa else "D"))
            except:
                continue
    return resultats[-nb_matchs:]


def get_serie_victoires(forme: list) -> int:
    """Retourne la série de victoires consécutives actuelles (depuis la fin)."""
    serie = 0
    for r in reversed(forme):
        if r == "V":
            serie += 1
        else:
            break
    return serie


def get_dernier_adversaire(history, saison, equipe):
    """Retourne le nom du dernier adversaire affronté (pour la Loi du Relâchement)."""
    journees = sorted(
        history[saison].keys(),
        key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0
    )
    for jk in reversed(journees):
        for match in history[saison][jk].get("res", []):
            if match.get("h") == equipe:
                return match.get("a")
            if match.get("a") == equipe:
                return match.get("h")
    return None


# ════════════════════════════════════════════════════════════
#  PERSISTENCE JSON
# ════════════════════════════════════════════════════════════

DB_FILE = "oracle_history.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if 'history' not in st.session_state:
    st.session_state['history'] = load_db()
    if not st.session_state['history']:
        st.session_state['history']["Saison 2026"] = {}


# ════════════════════════════════════════════════════════════
#  MOTEUR OCR
# ════════════════════════════════════════════════════════════

@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en', 'fr'], gpu=False)

reader = load_ocr()


class OracleEngine:
    def __init__(self):
        self.teams_list = [
            "Leeds", "Brighton", "A. Villa", "Manchester Blue", "C. Palace",
            "Bournemouth", "Spurs", "Burnley", "West Ham", "Liverpool",
            "Fulham", "Newcastle", "Manchester Red", "Everton", "London Blues",
            "Wolverhampton", "Sunderland", "N. Forest", "London Reds", "Brentford"
        ]

    def clean_team(self, text):
        m = get_close_matches(text, self.teams_list, n=1, cutoff=0.3)
        return m[0] if m else None

engine = OracleEngine()


# ════════════════════════════════════════════════════════════
#  EN-TÊTE
# ════════════════════════════════════════════════════════════

st.markdown("""
    <div class="main-header">
        <h1 class="header-title">🔮 Oracle Mahita</h1>
        <div class="header-subtitle">V34 · CERVEAU I ACTIF · PLAYBOOK STRATÉGIE</div>
    </div>
""", unsafe_allow_html=True)

col_l, col_m, col_r = st.columns([1, 1, 1])
with col_m:
    saisons = list(st.session_state['history'].keys())
    s_active = st.selectbox("Saison", saisons, label_visibility="collapsed")
    st.session_state['s_active'] = s_active

    days = [
        int(re.search(r'\d+', k).group())
        for k in st.session_state['history'][s_active].keys()
        if st.session_state['history'][s_active][k].get("res")
        and re.search(r'\d+', k)
    ]
    next_j = max(days) + 1 if days else 1
    st.markdown(f'<div class="next-day-box">PROCHAINE ÉTAPE : J-{next_j}</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  NAVIGATION — 7 ONGLETS
# ════════════════════════════════════════════════════════════

tabs = st.tabs([
    "🏆 CLASSEMENT",
    "📅 CALENDRIER",
    "🎯 PRONOS",
    "⚽ RÉSULTATS",
    "📚 HISTORIQUE",
    "⚙️ GESTION",
    "📊 PERFORMANCE & RATING"
])


# ════════════════════════════════════════════════════════════
#  TAB 0 — CLASSEMENT
# ════════════════════════════════════════════════════════════

with tabs[0]:
    st.markdown("### 🏆 Classement de la Saison")
    current_standings = get_standings(
        st.session_state['history'][s_active], engine.teams_list
    )

    # Colorisation du classement — compatible Pandas Styler
    def style_classement(row):
        rang = row['Rang']
        if rang <= 3:
            return ['background-color: rgba(0,255,0,0.1)'] * len(row)
        elif rang >= 17:
            return ['background-color: rgba(255,75,75,0.1)'] * len(row)
        else:
            return [''] * len(row)

    st.dataframe(
        current_standings.style.apply(style_classement, axis=1),
        use_container_width=True,
        hide_index=True
    )
    st.caption("🟢 Top 3 (Course au titre) · 🔴 Bas de classement (Zone de relégation)")


# ════════════════════════════════════════════════════════════
#  TAB 1 — CALENDRIER (OCR + Saisie manuelle)
# ════════════════════════════════════════════════════════════

with tabs[1]:
    st.markdown("### 📅 Import du Calendrier")
    j_cal = st.number_input("Journée", 1, 50, next_j)
    f_cal = st.file_uploader("📸 Sélectionner l'image du Calendrier", type=['jpg','png','jpeg'], key="up_cal")

    if f_cal:
        with st.spinner("🔍 Lecture OCR en cours..."):
            image_bytes = f_cal.getvalue()
            res = reader.readtext(image_bytes, detail=0)

        t_f, o_f = [], []
        for t in res:
            n = engine.clean_team(t)
            if n:
                t_f.append(n)
            for val in re.findall(r"\d+[\.,]\d+", t):
                o_f.append(float(val.replace(',', '.')))

        st.session_state['tmp_cal'] = []
        for i in range(10):
            h = t_f[i*2]   if len(t_f) > i*2   else "Inconnu"
            a = t_f[i*2+1] if len(t_f) > i*2+1 else "Inconnu"
            o = o_f[i*3:i*3+3]
            st.session_state['tmp_cal'].append({
                'h': h, 'a': a,
                'o': [
                    o[0] if len(o) > 0 else 1.80,
                    o[1] if len(o) > 1 else 3.50,
                    o[2] if len(o) > 2 else 4.00
                ]
            })
        custom_notify("✅ OCR terminé — vérifiez et corrigez si nécessaire", color="#7FFFD4")

    # Saisie manuelle si pas d'OCR
    if 'tmp_cal' not in st.session_state:
        if st.button("✏️ Saisie manuelle (sans image)"):
            st.session_state['tmp_cal'] = [
                {'h': engine.teams_list[i*2], 'a': engine.teams_list[i*2+1], 'o': [1.80, 3.50, 4.00]}
                for i in range(10)
            ]

    if 'tmp_cal' in st.session_state:
        with st.form("form_cal"):
            st.markdown("#### Vérifiez et corrigez les matchs :")
            final_c = []
            for i, m in enumerate(st.session_state['tmp_cal']):
                st.markdown(f"**Match {i+1}**")
                c1, c2, o1, ox, o2 = st.columns([2, 2, 1, 1, 1])
                th = c1.selectbox(
                    f"Domicile {i+1}", engine.teams_list,
                    index=engine.teams_list.index(m['h']) if m['h'] in engine.teams_list else 0,
                    key=f"h_{i}"
                )
                ta = c2.selectbox(
                    f"Extérieur {i+1}", engine.teams_list,
                    index=engine.teams_list.index(m['a']) if m['a'] in engine.teams_list else 0,
                    key=f"a_{i}"
                )
                c1_val = o1.number_input("Cote 1", value=float(m['o'][0]), min_value=1.0, step=0.05, key=f"o1_{i}")
                cx_val = ox.number_input("Cote X", value=float(m['o'][1]), min_value=1.0, step=0.05, key=f"ox_{i}")
                c2_val = o2.number_input("Cote 2", value=float(m['o'][2]), min_value=1.0, step=0.05, key=f"o2_{i}")
                final_c.append({'h': th, 'a': ta, 'o': [c1_val, cx_val, c2_val]})

            if st.form_submit_button("🔥 VALIDER & ENREGISTRER"):
                jk = f"Journée {j_cal}"
                if jk not in st.session_state['history'][s_active]:
                    st.session_state['history'][s_active][jk] = {"cal": [], "res": [], "pro": [], "rank": []}
                st.session_state['history'][s_active][jk]["cal"] = final_c
                st.session_state['current_ready'] = final_c
                st.session_state['current_j_num'] = j_cal
                save_db(st.session_state['history'])
                # Nettoyer le tmp pour éviter de re-afficher le formulaire
                if 'tmp_cal' in st.session_state:
                    del st.session_state['tmp_cal']
                custom_notify("✅ Calendrier enregistré ! Allez dans l'onglet PRONOS 🎯")


# ════════════════════════════════════════════════════════════
#  TAB 2 — PRONOS (CERVEAU I INTÉGRÉ)
# ════════════════════════════════════════════════════════════

with tabs[2]:
    st.markdown("### 🎯 Analyse & Pronos — Cerveau I")

    if 'current_ready' not in st.session_state:
        st.info("📅 Veuillez d'abord valider un calendrier dans l'onglet CALENDRIER.")
    else:
        safe_d, risque_d, fun_d = [], [], []
        j_num = st.session_state.get('current_j_num', 1)

        # Classement actuel pour les rangs
        standings = get_standings(
            st.session_state['history'][s_active], engine.teams_list
        )

        st.markdown(f"**Journée {j_num}** — {len(st.session_state['current_ready'])} matchs analysés par le Cerveau I")
        st.divider()

        for m in st.session_state['current_ready']:

            # ── Récupération des données contextuelles ──────────
            r_dom = int(standings[standings['Équipe'] == m['h']]['Rang'].values[0]) \
                    if m['h'] in standings['Équipe'].values else 10
            r_ext = int(standings[standings['Équipe'] == m['a']]['Rang'].values[0]) \
                    if m['a'] in standings['Équipe'].values else 10

            forme_dom = get_forme_equipe(
                st.session_state['history'], s_active, m['h']
            )
            forme_ext = get_forme_equipe(
                st.session_state['history'], s_active, m['a']
            )
            serie_dom = get_serie_victoires(forme_dom)
            serie_ext = get_serie_victoires(forme_ext)
            dernier_adv_dom = get_dernier_adversaire(
                st.session_state['history'], s_active, m['h']
            )

            # ── Appel au Cerveau I ───────────────────────────────
            analyse = oracle_brain.analyser_match(
                equipe_dom=m['h'],
                equipe_ext=m['a'],
                cotes=m['o'],
                journee=j_num,
                rang_dom=r_dom,
                rang_ext=r_ext,
                serie_dom=serie_dom,
                serie_ext=serie_ext,
                forme_dom=forme_dom,
                forme_ext=forme_ext,
                match_precedent_dom=dernier_adv_dom
            )

            # ── Affichage du match ───────────────────────────────
            confiance = analyse['indice_confiance']
            classe = analyse['confiance']

            if classe == "BANKER":
                badge_color = "indice-banker"
                emoji_classe = "🟢"
            elif classe == "RISQUE CALCULÉ":
                badge_color = "indice-risque"
                emoji_classe = "🟡"
            else:
                badge_color = "indice-fun"
                emoji_classe = "🔴"

            with st.container():
                col_info, col_indice = st.columns([3, 1])

                with col_info:
                    st.markdown(f"⚽ **{m['h']}** vs **{m['a']}**")
                    # Forme des équipes
                    forme_dom_str = " ".join(
                        [f"{'🟢' if r=='V' else ('🟡' if r=='N' else '🔴')}" for r in forme_dom[-5:]]
                    ) if forme_dom else "— pas d'historique"
                    forme_ext_str = " ".join(
                        [f"{'🟢' if r=='V' else ('🟡' if r=='N' else '🔴')}" for r in forme_ext[-5:]]
                    ) if forme_ext else "— pas d'historique"

                    st.caption(f"🏠 {m['h']} : {forme_dom_str}  |  ✈️ {m['a']} : {forme_ext_str}")
                    st.caption(f"Cotes : 1={m['o'][0]} · X={m['o'][1]} · 2={m['o'][2]}  |  Rangs : {m['h']} {r_dom}e · {m['a']} {r_ext}e")

                with col_indice:
                    st.markdown(
                        f"<div class='{badge_color}'>{emoji_classe} {confiance}%<br><small>{classe}</small></div>",
                        unsafe_allow_html=True
                    )

                # Alertes du Cerveau I
                with st.expander(f"🧠 Analyse Cerveau I — {analyse['choix_expert']}"):
                    for alerte in analyse['alertes']:
                        if any(k in alerte for k in ["🚨","⚠️","🔔","😮"]):
                            st.markdown(f"<div class='alerte-danger'>{alerte}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='alerte-oracle'>{alerte}</div>", unsafe_allow_html=True)

                    # Détail des modules
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.markdown("<div class='module-box'>", unsafe_allow_html=True)
                        st.caption("**Module 1 — Forme**")
                        st.write(f"DOM : {analyse['modules']['trajectoire_dom']['score_forme']}/100")
                        st.write(f"EXT : {analyse['modules']['trajectoire_ext']['score_forme']}/100")
                        st.markdown("</div>", unsafe_allow_html=True)
                    with col_m2:
                        st.markdown("<div class='module-box'>", unsafe_allow_html=True)
                        st.caption("**Module 2 — Enjeu**")
                        st.write(f"DOM : {analyse['modules']['mss_dom']['enjeu']}")
                        st.write(f"EXT : {analyse['modules']['mss_ext']['enjeu']}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    with col_m3:
                        st.markdown("<div class='module-box'>", unsafe_allow_html=True)
                        st.caption("**Module 3 — Fatigue**")
                        st.write(f"Série DOM : {serie_dom} V")
                        st.write(f"Série EXT : {serie_ext} V")
                        st.markdown("</div>", unsafe_allow_html=True)

            st.divider()

            # Distribution dans les tickets
            item = {
                "txt": analyse['choix_expert'],
                "cote": max(m['o']),
                "match": f"{m['h']} vs {m['a']}",
                "indice": confiance
            }
            if classe == "BANKER":
                safe_d.append(item)
            elif classe == "RISQUE CALCULÉ":
                risque_d.append(item)
            else:
                fun_d.append(item)

        # ── Enregistrement des pronos dans l'historique ──────
        jk_prono = f"Journée {j_num}"
        if jk_prono in st.session_state['history'][s_active]:
            pronos_a_sauver = []
            for m in st.session_state['current_ready']:
                analyse_save = oracle_brain.analyser_match(
                    equipe_dom=m['h'], equipe_ext=m['a'], cotes=m['o'],
                    journee=j_num,
                    rang_dom=int(standings[standings['Équipe']==m['h']]['Rang'].values[0])
                        if m['h'] in standings['Équipe'].values else 10,
                    rang_ext=int(standings[standings['Équipe']==m['a']]['Rang'].values[0])
                        if m['a'] in standings['Équipe'].values else 10,
                    forme_dom=get_forme_equipe(st.session_state['history'], s_active, m['h']),
                    forme_ext=get_forme_equipe(st.session_state['history'], s_active, m['a']),
                )
                pronos_a_sauver.append({
                    "m": analyse_save['choix_expert'],
                    "c": m['o'],
                    "indice": analyse_save['indice_confiance'],
                    "classe": analyse_save['confiance']
                })
            st.session_state['history'][s_active][jk_prono]["pro"] = pronos_a_sauver
            save_db(st.session_state['history'])

        # ── TICKETS ─────────────────────────────────────────
        st.markdown("## 🎟️ Tickets Oracle")
        c1, c2, c3 = st.columns(3)

        def show_ticket(col, title, css_class, data, emoji):
            with col:
                st.markdown(f"### {emoji} {title}")
                if not data:
                    st.write("Aucun match dans ce ticket.")
                    return
                total_cote = 1.0
                for x in data[:3]:
                    st.markdown(
                        f"""<div class="{css_class}">
                        <b>{x['match']}</b><br>
                        {x['txt']}<br>
                        <small>Indice : {x['indice']}%</small>
                        </div>""",
                        unsafe_allow_html=True
                    )
                    total_cote *= x['cote']
                st.info(f"⚡ Ticket {title} · Cote combinée ≈ {total_cote:.2f}")

        show_ticket(c1, "TICKET SAFE",   "prono-safe",   safe_d,   "🟢")
        show_ticket(c2, "TICKET RISQUE", "prono-risque", risque_d, "🟡")
        show_ticket(c3, "TICKET FUN",    "prono-fun",    fun_d,    "🔴")


# ════════════════════════════════════════════════════════════
#  TAB 3 — RÉSULTATS
# ════════════════════════════════════════════════════════════

with tabs[3]:
    st.markdown("### ⚽ Saisie des Résultats")
    j_res = st.number_input("Journée Résultat", 1, 50, 1, key="jres")
    f_res = st.file_uploader("📸 Scan Résultats (optionnel)", type=['jpg','png','jpeg'])

    extracted_matches = []

    if f_res:
        with st.spinner("🔍 Lecture OCR des résultats..."):
            img = Image.open(f_res)
            w, hi = img.size
            mid = w / 2
            raw = reader.readtext(f_res.getvalue(), detail=1)
            raw.sort(key=lambda x: x[0][0][1])

        tms = [
            t for t in [
                {"n": engine.clean_team(txt), "y": b[0][1], "x": (b[0][0]+b[1][0])/2}
                for (b, txt, p) in raw
            ]
            if t["n"] and hi*0.12 < t["y"] < hi*0.95
        ]
        ancs = []
        for t in tms:
            if t["x"] < mid and (not ancs or abs(t["y"] - ancs[-1]["y"]) > 45):
                ancs.append(t)

        for i, a in enumerate(ancs):
            if len(extracted_matches) >= 10:
                break
            ys = a["y"] - 15
            ye = (ancs[i+1]["y"] - 15 if i+1 < len(ancs) else hi * 0.98)
            inf = {"h": a["n"], "a": "Inconnu", "s": "0:0", "hm": "", "am": "", "mt": ""}
            for (bb, tx, p) in raw:
                cy = (bb[0][1]+bb[2][1])/2
                cx = (bb[0][0]+bb[1][0])/2
                if ys <= cy <= ye:
                    tn = engine.clean_team(tx)
                    if tn and cx > mid and tn != inf["h"]:
                        inf["a"] = tn
                    elif re.search(r"^\d[:\-]\d$", tx.strip()) and "MT" not in tx.upper():
                        inf["s"] = tx
                    elif "MT" in tx.upper():
                        inf["mt"] = tx
                    elif re.search(r"\d+", tx) and not re.search(r"^\d[:\-]\d$", tx):
                        if cx < mid:
                            inf["hm"] += f" {tx}'"
                        else:
                            inf["am"] += f" {tx}'"
            if inf["a"] != "Inconnu":
                extracted_matches.append(inf)

    else:
        # Saisie manuelle depuis le calendrier enregistré
        jk_res = f"Journée {j_res}"
        cal_data = st.session_state['history'][s_active].get(jk_res, {}).get("cal", [])
        for m in cal_data:
            extracted_matches.append({"h": m["h"], "a": m["a"], "s": "0:0", "hm": "", "am": "", "mt": ""})

    with st.form("res_val_form"):
        final_res_data = []
        if not extracted_matches:
            st.info("📋 Importez une image ou vérifiez que le calendrier de cette journée est enregistré.")
        for i, r in enumerate(extracted_matches):
            st.markdown(f"**{r['h']} vs {r['a']}**")
            c1, c2 = st.columns(2)
            fs = c1.text_input("Score Final (ex: 2:1)", r['s'], key=f"rs{i}")
            ms = c2.text_input("Score MT (ex: 1:0)", r.get('mt',''), key=f"rm{i}")
            b1, b2 = st.columns(2)
            bh = b1.text_input("Buteurs Domicile", r.get('hm',''), key=f"rbh{i}")
            ba = b2.text_input("Buteurs Extérieur", r.get('am',''), key=f"rba{i}")
            final_res_data.append({"h": r['h'], "a": r['a'], "s": fs, "mt": ms, "hm": bh, "am": ba})

        if st.form_submit_button("✅ ENREGISTRER LES RÉSULTATS"):
            sn = st.session_state['s_active']
            jk = f"Journée {j_res}"
            if jk not in st.session_state['history'][sn]:
                st.session_state['history'][sn][jk] = {"cal": [], "res": [], "pro": []}
            st.session_state['history'][sn][jk]["res"] = final_res_data
            save_db(st.session_state['history'])
            custom_notify("✅ Résultats enregistrés ! Le Cerveau I va apprendre de ces données 🧠")


# ════════════════════════════════════════════════════════════
#  TAB 4 — HISTORIQUE
# ════════════════════════════════════════════════════════════

with tabs[4]:
    st.markdown("### 📚 Historique des Journées")
    sorted_j = sorted(
        st.session_state['history'][s_active].keys(),
        key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0
    )
    for jk in sorted_j:
        with st.expander(f"📅 {jk}"):
            d = st.session_state['history'][s_active][jk]
            h_tabs = st.tabs(["📋 Calendrier", "🎯 Prono", "⚽ Résultat"])

            with h_tabs[0]:
                if d.get("cal"):
                    st.table(pd.DataFrame(d["cal"]))
                    if st.button(f"🔮 Relancer les Pronos", key=f"sim_{jk}"):
                        st.session_state['current_ready'] = d["cal"]
                        st.session_state['current_j_num'] = int(re.search(r'\d+', jk).group())
                        st.rerun()
                else:
                    st.write("Aucun calendrier enregistré.")

            with h_tabs[1]:
                pronos = d.get("pro", [])
                if pronos:
                    df_pro = pd.DataFrame(pronos)
                    st.table(df_pro)
                else:
                    st.write("Aucun prono enregistré.")

            with h_tabs[2]:
                res = d.get("res", [])
                if res:
                    st.table(pd.DataFrame(res))
                else:
                    st.write("Aucun résultat enregistré.")


# ════════════════════════════════════════════════════════════
#  TAB 5 — GESTION
# ════════════════════════════════════════════════════════════

with tabs[5]:
    st.markdown("### ⚙️ Gestion des Saisons")

    col_new, col_del = st.columns(2)
    with col_new:
        ns = st.text_input("Nom de la nouvelle Saison (ex: Saison 2027)")
        if st.button("➕ Créer la Saison"):
            if ns and ns not in st.session_state['history']:
                st.session_state['history'][ns] = {}
                save_db(st.session_state['history'])
                st.rerun()
            elif not ns:
                st.warning("Entrez un nom de saison.")
            else:
                st.warning("Cette saison existe déjà.")

    st.divider()

    # Import backup
    st.markdown("#### 📥 Backup & Restauration")
    col_exp, col_imp = st.columns(2)
    with col_exp:
        if st.session_state['history']:
            st.download_button(
                "📥 Exporter Backup JSON",
                data=json.dumps(st.session_state['history'], indent=4, ensure_ascii=False),
                file_name="oracle_backup.json",
                mime="application/json"
            )
    with col_imp:
        uploaded_backup = st.file_uploader("📤 Importer un Backup", type=["json"], key="backup_import")
        if uploaded_backup:
            try:
                backup_data = json.load(uploaded_backup)
                st.session_state['history'] = backup_data
                save_db(backup_data)
                custom_notify("✅ Backup importé avec succès !", color="#7FFFD4")
                st.rerun()
            except Exception as e:
                st.error(f"Erreur lors de l'import : {e}")


# ════════════════════════════════════════════════════════════
#  TAB 6 — PERFORMANCE & RATING
# ════════════════════════════════════════════════════════════

with tabs[6]:
    st.markdown("""
        <div class='main-header'>
            <h1 class='header-title'>📊 RATING & PERFORMANCE</h1>
        </div>
    """, unsafe_allow_html=True)

    stats_perf = oracle_brain.calculer_performance_globale(
        st.session_state['history'][s_active]
    )

    if stats_perf["total_matchs"] == 0:
        st.info("ℹ️ L'Oracle a besoin de résultats pour calculer son rating. Enregistrez des résultats dans l'onglet RÉSULTATS.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("⚽ Matchs analysés",   stats_perf["total_matchs"])
        c2.metric("🎯 Réussite 1N2",      f"{stats_perf['taux_1n2']:.1f}%")
        c3.metric("💎 Scores Exacts",     stats_perf["scores_exacts"])
        c4.metric("📈 Points/Match",      f"{stats_perf['moyenne_points']:.2f}")

        st.divider()

        rating = stats_perf["rating_general"]
        color  = "green" if rating >= 80 else ("orange" if rating >= 50 else "red")

        st.markdown(f"**Score Global Oracle :**")
        st.progress(int(rating) / 100)
        st.markdown(
            f"<span style='color:{color}; font-size:28px; font-weight:900;'>{rating:.1f} / 100</span>",
            unsafe_allow_html=True
        )

        st.divider()

        # Analyse de forme par équipe
        st.markdown("#### 🔍 Forme actuelle des équipes")
        forme_data = []
        for equipe in engine.teams_list:
            forme = get_forme_equipe(st.session_state['history'], s_active, equipe)
            if forme:
                score = sum({"V":3,"N":1,"D":0}.get(r,0) for r in forme)
                score_pct = int((score / (len(forme)*3)) * 100)
                serie = get_serie_victoires(forme)
                forme_data.append({
                    "Équipe": equipe,
                    "Forme": " ".join(forme[-5:]),
                    "Score": f"{score_pct}%",
                    "Série V": serie
                })
        if forme_data:
            st.dataframe(pd.DataFrame(forme_data), use_container_width=True, hide_index=True)
        else:
            st.info("Enregistrez des résultats pour voir la forme des équipes.")
