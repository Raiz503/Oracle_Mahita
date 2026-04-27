"""
╔══════════════════════════════════════════════════════════════╗
║         ORACLE MAHITA — CERVEAU I : PLAYBOOK STRATÉGIE       ║
║         Basé sur le Manuel de Stratégie (Saison Clôturée)    ║
║         Version 1.0                                          ║
╚══════════════════════════════════════════════════════════════╝

4 Piliers :
  Module 1 — Trajectoire 6   : Dynamique de forme (Momentum ±15%)
  Module 2 — MSS (Surprise)  : Enjeux vitaux Titre/Maintien
  Module 3 — Fatigue/Cycle   : Plafond de 3 victoires consécutives
  Module 4 — Décision        : Indice de Value vs cotes marché
"""

# ─────────────────────────────────────────────
#  ADN DES ÉQUIPES (Profils comportementaux)
# ─────────────────────────────────────────────

PROFILS_EQUIPES = {
    # Profil "Vertical" — séries longues, sensibles face-à-face
    "London Reds":       {"profil": "Vertical",    "serie_max": 4, "sensibilite_face_a_face": True,  "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
    "Manchester Blue":   {"profil": "Vertical",    "serie_max": 4, "sensibilite_face_a_face": True,  "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},

    # Profil "Explosif" — pics offensifs puis 0-0 illogiques
    "Liverpool":         {"profil": "Explosif",    "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": True,  "giant_killer": False, "lineaire": False, "defensif_nul": False},

    # Profil "Giant Killer" — casse les trajectoires des favoris
    "Brentford":         {"profil": "Giant Killer","serie_max": 2, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": True,  "lineaire": False, "defensif_nul": False},

    # Profil "Linéaire" — très prévisibles, suivent leur courbe
    "Everton":           {"profil": "Linéaire",    "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": True,  "defensif_nul": False},
    "A. Villa":          {"profil": "Linéaire",    "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": True,  "defensif_nul": False},

    # Profil "Lanterne" — faible défense, nuls de blocage quand adversaire fatigué
    "Sunderland":        {"profil": "Lanterne",    "serie_max": 1, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": True},

    # Profils neutres pour les équipes non encore caractérisées
    "Leeds":             {"profil": "Neutre", "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
    "Brighton":          {"profil": "Neutre", "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
    "Bournemouth":       {"profil": "Neutre", "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
    "Spurs":             {"profil": "Neutre", "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
    "Burnley":           {"profil": "Neutre", "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
    "West Ham":          {"profil": "Neutre", "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
    "Fulham":            {"profil": "Neutre", "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
    "Newcastle":         {"profil": "Neutre", "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
    "Manchester Red":    {"profil": "Neutre", "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
    "London Blues":      {"profil": "Neutre", "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
    "Wolverhampton":     {"profil": "Neutre", "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
    "N. Forest":         {"profil": "Neutre", "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
    "C. Palace":         {"profil": "Neutre", "serie_max": 3, "sensibilite_face_a_face": False, "instabilite_offensive": False, "giant_killer": False, "lineaire": False, "defensif_nul": False},
}

# ─────────────────────────────────────────────
#  SEUILS ET CONSTANTES DU PLAYBOOK
# ─────────────────────────────────────────────

# Module 1 — Trajectoire 6
MOMENTUM_BONUS          = 0.15   # +15% si bonne forme récente
MOMENTUM_MALUS          = -0.15  # -15% si mauvaise forme récente

# Module 2 — MSS (Survie / Titre)
JOURNEE_SURVIE_DEBUT    = 34     # Activation de la Loi de Survie
JOURNEE_SURVIE_FIN      = 38
RANG_RELEGABLE_MIN      = 17     # Positions relégables
RANG_RELEGABLE_MAX      = 20
BONUS_SURVIE_RESILIENCE = 0.25   # +25% résilience pour équipe relégable

RANG_TITRE_MAX          = 3      # Top 3 = en course pour le titre
BONUS_TITRE             = 0.10   # +10% motivation titre

# Module 3 — Fatigue / Plafond de Verre
PLAFOND_SERIE_VICTOIRES = 3      # Alerte après 3 victoires consécutives
BONUS_NUL_APRES_SERIE   = 0.12   # +12% probabilité nul au 4ème match

# Module 4 — Indice de confiance
SEUIL_BANKER            = 80     # 80-95% → BANKER
SEUIL_RISQUE            = 60     # 60-79% → Risque Calculé
# < 60%                          → Ticket Fun

# Loi du Relâchement Post-Sommet
MALUS_RELACHEMENT_MIN   = 0.05   # -5% efficacité offensive
MALUS_RELACHEMENT_MAX   = 0.08   # -8% efficacité offensive

# ─────────────────────────────────────────────
#  CLASSE PRINCIPALE : CERVEAU I
# ─────────────────────────────────────────────

class CerveauI:
    """
    Cerveau I — Pilier Stratégique (Playbook)
    Implémente les 4 modules et les Lois de l'Oracle.
    """

    def __init__(self):
        self.profils = PROFILS_EQUIPES

    # ══════════════════════════════════════════
    #  MODULE 1 — TRAJECTOIRE 6 (Momentum)
    # ══════════════════════════════════════════

    def module1_trajectoire(self, resultats_recents: list) -> dict:
        """
        Analyse la dynamique de forme sur les 6 derniers matchs.

        Args:
            resultats_recents : liste de résultats récents, ex: ['V','V','N','D','V','V']
                                (du plus ancien au plus récent)
                                V = Victoire, N = Nul, D = Défaite

        Returns:
            dict avec momentum, score_forme, alertes
        """
        if not resultats_recents:
            return {"momentum": 0.0, "score_forme": 50, "serie": 0, "alertes": []}

        # On prend les 6 derniers matchs maximum
        recents = resultats_recents[-6:]

        # Calcul du score de forme (/100)
        points = {"V": 3, "N": 1, "D": 0}
        total_points = sum(points.get(r.upper(), 0) for r in recents)
        score_forme = int((total_points / (len(recents) * 3)) * 100)

        # Calcul du momentum
        if score_forme >= 65:
            momentum = MOMENTUM_BONUS
        elif score_forme <= 35:
            momentum = MOMENTUM_MALUS
        else:
            momentum = 0.0

        # Calcul de la série en cours (depuis la fin)
        serie = 0
        dernier = recents[-1].upper() if recents else None
        if dernier in ("V", "D", "N"):
            for r in reversed(recents):
                if r.upper() == dernier:
                    serie += 1
                else:
                    break

        alertes = []
        if score_forme >= 80:
            alertes.append("🔥 Excellente forme — momentum offensif fort")
        elif score_forme <= 25:
            alertes.append("❄️ Mauvaise forme — méfiance même si favori")

        return {
            "momentum": momentum,
            "score_forme": score_forme,
            "serie": serie,
            "dernier_resultat": dernier,
            "alertes": alertes
        }

    # ══════════════════════════════════════════
    #  MODULE 2 — MSS (MOTIVATION / SURVIE)
    # ══════════════════════════════════════════

    def module2_mss(self, rang: int, journee: int, rang_adversaire: int = 10) -> dict:
        """
        Détecte les enjeux vitaux : maintien, titre, Europa, relégation.

        Args:
            rang          : classement actuel de l'équipe (1=premier)
            journee       : numéro de journée actuelle
            rang_adversaire : classement de l'équipe adverse

        Returns:
            dict avec bonus_motivation, enjeu, alertes
        """
        alertes = []
        bonus_motivation = 0.0
        enjeu = "Standard"

        # Loi de Survie Critique (J34-J38 pour les relégables)
        if JOURNEE_SURVIE_DEBUT <= journee <= JOURNEE_SURVIE_FIN:
            if RANG_RELEGABLE_MIN <= rang <= RANG_RELEGABLE_MAX:
                bonus_motivation += BONUS_SURVIE_RESILIENCE
                enjeu = "SURVIE CRITIQUE"
                alertes.append(f"🚨 LOI DE SURVIE — Équipe {rang}e en zone rouge (J{journee}) : +25% résilience")
                alertes.append("⚠️ Ne jamais parier SEC sur le favori — couvrir avec le Nul (1N ou N2)")

            # Même logique si l'adversaire est relégable
            if RANG_RELEGABLE_MIN <= rang_adversaire <= RANG_RELEGABLE_MAX:
                alertes.append(f"⚠️ L'adversaire est aussi en survie (rang {rang_adversaire}e) — match très ouvert")

        # Course au Titre (Top 3)
        if rang <= RANG_TITRE_MAX:
            bonus_motivation += BONUS_TITRE
            enjeu = "COURSE AU TITRE"
            alertes.append(f"🏆 Course au titre — motivation maximale (rang {rang}e)")

        # Période sans enjeu (mi-saison, équipe mid-table)
        if 8 <= rang <= 14 and journee < 30:
            enjeu = "Sans enjeu"
            alertes.append("😐 Équipe sans enjeu — attention aux matchs relâchés")

        return {
            "bonus_motivation": bonus_motivation,
            "enjeu": enjeu,
            "alertes": alertes
        }

    # ══════════════════════════════════════════
    #  MODULE 3 — FATIGUE / PLAFOND DE VERRE
    # ══════════════════════════════════════════

    def module3_fatigue(self, serie_victoires: int, equipe: str, equipe_adverse: str) -> dict:
        """
        Anticipe la chute après surperformance et les chocs émotionnels.

        Args:
            serie_victoires : nombre de victoires consécutives actuelles
            equipe          : nom de l'équipe à analyser
            equipe_adverse  : nom de l'adversaire

        Returns:
            dict avec alerte_plafond, malus_relachement, alertes
        """
        alertes = []
        alerte_plafond = False
        malus_relachement = 0.0
        bonus_nul = 0.0

        # Plafond de Verre — 3 victoires consécutives
        if serie_victoires >= PLAFOND_SERIE_VICTOIRES:
            alerte_plafond = True
            bonus_nul = BONUS_NUL_APRES_SERIE
            alertes.append(f"🔔 PLAFOND DE VERRE — {equipe} : {serie_victoires} victoires de suite !")
            alertes.append("📊 Probabilité du Nul (X) augmente de +12% — chercher la Value sur le match nul")

        # Loi du Relâchement Post-Sommet
        # Détection d'un choc émotionnel (derby ou match au sommet)
        chocs = [
            ("Manchester Blue", "London Reds"),
            ("London Reds", "Manchester Blue"),
            ("Liverpool", "Manchester Blue"),
            ("Manchester Blue", "Liverpool"),
            ("London Reds", "Liverpool"),
        ]
        est_post_sommet = False
        for e1, e2 in chocs:
            if equipe == e1 and equipe_adverse == e2:
                est_post_sommet = True
                break

        if est_post_sommet:
            malus_relachement = (MALUS_RELACHEMENT_MIN + MALUS_RELACHEMENT_MAX) / 2  # moyenne: 6.5%
            alertes.append(f"😮‍💨 LOI DU RELÂCHEMENT — {equipe} sort d'un choc émotionnel majeur")
            alertes.append("💡 Privilégier la Double Chance plutôt qu'un pari sec")

        # Giant Killer — Brentford contre un favori
        profil_adv = self.profils.get(equipe_adverse, {})
        profil_eq  = self.profils.get(equipe, {})

        if profil_eq.get("giant_killer") and profil_adv.get("profil") in ("Vertical", "Explosif"):
            alertes.append(f"🗡️ GIANT KILLER — {equipe} peut surprendre {equipe_adverse} !")

        # Instabilité offensive (Liverpool)
        if profil_eq.get("instabilite_offensive"):
            alertes.append(f"🎲 INSTABILITÉ OFFENSIVE — {equipe} imprévisible : pic de buts ou 0-0 possible")

        # Nul de blocage (Sunderland fatigué vs adversaire fatigué)
        if profil_eq.get("defensif_nul"):
            alertes.append(f"🛡️ NUL DE BLOCAGE POSSIBLE — {equipe} peut tenir 0-0 si l'adversaire est fatigué")

        return {
            "alerte_plafond": alerte_plafond,
            "malus_relachement": malus_relachement,
            "bonus_nul": bonus_nul,
            "alertes": alertes
        }

    # ══════════════════════════════════════════
    #  MODULE 4 — DÉCISION (INDICE DE CONFIANCE)
    # ══════════════════════════════════════════

    def module4_decision(self, score_base: float, bonus_total: float, malus_total: float) -> dict:
        """
        Calcule l'Indice de Confiance final et la classification du pari.

        Args:
            score_base   : score de base (0-100), ex: 70 pour un favori modéré
            bonus_total  : cumul des bonus des modules 1, 2, 3 (en décimal, ex: 0.35)
            malus_total  : cumul des malus (en décimal, ex: 0.065)

        Returns:
            dict avec indice_confiance, classification, recommandation, alertes
        """
        # Application des bonus/malus au score de base
        ajustement = (bonus_total - malus_total) * 100
        indice = min(95, max(10, score_base + ajustement))

        # Classification selon les seuils du Playbook
        if indice >= SEUIL_BANKER:
            classification = "BANKER"
            recommandation = "Mise forte recommandée"
            emoji = "🟢"
        elif indice >= SEUIL_RISQUE:
            classification = "RISQUE CALCULÉ"
            recommandation = "Mise modérée — surveiller les alertes"
            emoji = "🟡"
        else:
            classification = "TICKET FUN"
            recommandation = "Petite mise — cote haute, surprise possible"
            emoji = "🔴"

        alertes = [f"{emoji} Indice de confiance : {indice:.1f}% → {classification}"]

        return {
            "indice_confiance": round(indice, 1),
            "classification": classification,
            "recommandation": recommandation,
            "alertes": alertes
        }

    # ══════════════════════════════════════════
    #  ANALYSE COMPLÈTE D'UN MATCH
    # ══════════════════════════════════════════

    def analyser_match(
        self,
        equipe_dom: str,
        equipe_ext: str,
        cotes: list,
        journee: int,
        rang_dom: int = 10,
        rang_ext: int = 10,
        serie_dom: int = 0,
        serie_ext: int = 0,
        forme_dom: list = None,
        forme_ext: list = None,
        match_precedent_dom: str = None  # Adversaire du dernier match (pour Loi Relâchement)
    ) -> dict:
        """
        Point d'entrée principal — analyse complète d'un match avec les 4 modules.

        Args:
            equipe_dom   : nom équipe domicile
            equipe_ext   : nom équipe extérieur
            cotes        : [cote_1, cote_X, cote_2]
            journee      : numéro de journée
            rang_dom     : classement équipe domicile
            rang_ext     : classement équipe extérieur
            serie_dom    : série victoires consécutives domicile
            serie_ext    : série victoires consécutives extérieur
            forme_dom    : liste résultats récents domicile ex: ['V','V','N','D','V']
            forme_ext    : liste résultats récents extérieur
            match_precedent_dom : adversaire du dernier match (pour détecter post-sommet)

        Returns:
            dict complet avec tous les modules, alertes, et décision finale
        """
        forme_dom = forme_dom or []
        forme_ext = forme_ext or []
        alertes_globales = []

        # ── Module 1 : Trajectoire ──
        traj_dom = self.module1_trajectoire(forme_dom)
        traj_ext = self.module1_trajectoire(forme_ext)
        alertes_globales += [f"[DOM] {a}" for a in traj_dom["alertes"]]
        alertes_globales += [f"[EXT] {a}" for a in traj_ext["alertes"]]

        # ── Module 2 : MSS ──
        mss_dom = self.module2_mss(rang_dom, journee, rang_ext)
        mss_ext = self.module2_mss(rang_ext, journee, rang_dom)
        alertes_globales += [f"[DOM] {a}" for a in mss_dom["alertes"]]
        alertes_globales += [f"[EXT] {a}" for a in mss_ext["alertes"]]

        # ── Module 3 : Fatigue ──
        # Adversaire du match précédent pour détecter le relâchement
        adv_prec_dom = match_precedent_dom or equipe_ext
        fat_dom = self.module3_fatigue(serie_dom, equipe_dom, adv_prec_dom)
        fat_ext = self.module3_fatigue(serie_ext, equipe_ext, equipe_dom)
        alertes_globales += [f"[DOM] {a}" for a in fat_dom["alertes"]]
        alertes_globales += [f"[EXT] {a}" for a in fat_ext["alertes"]]

        # ── Calcul du score de base depuis les cotes ──
        cote_1, cote_x, cote_2 = cotes[0], cotes[1], cotes[2]
        prob_1 = (1 / cote_1) * 100
        prob_x = (1 / cote_x) * 100
        prob_2 = (1 / cote_2) * 100

        # Favori = équipe avec la plus haute probabilité implicite
        if prob_1 >= prob_2:
            favori = equipe_dom
            score_base = prob_1
            bonus_favori = traj_dom["momentum"] + mss_dom["bonus_motivation"]
            malus_favori = fat_dom["malus_relachement"]
        else:
            favori = equipe_ext
            score_base = prob_2
            bonus_favori = traj_ext["momentum"] + mss_ext["bonus_motivation"]
            malus_favori = fat_ext["malus_relachement"]

        # Bonus nul (plafond de verre des deux équipes)
        bonus_nul = max(fat_dom["bonus_nul"], fat_ext["bonus_nul"])

        # ── Module 4 : Décision ──
        decision = self.module4_decision(score_base, bonus_favori, malus_favori)
        alertes_globales += decision["alertes"]

        # ── Choix expert final ──
        if bonus_nul >= BONUS_NUL_APRES_SERIE:
            choix_expert = f"Match Nul (X) — Value sur le {cote_x}"
            alertes_globales.append("🎯 Recommandation : parier sur le Nul pour la Value")
        elif prob_1 >= prob_2:
            choix_expert = f"Victoire {equipe_dom} (1) — cote {cote_1}"
        else:
            choix_expert = f"Victoire {equipe_ext} (2) — cote {cote_2}"

        # Couverture MSS (survie vs favori)
        if mss_ext["enjeu"] == "SURVIE CRITIQUE" and prob_1 > prob_2:
            choix_expert = f"Double Chance 1X — Ne pas parier sec sur {equipe_dom}"
            alertes_globales.append("🛡️ Couverture MSS : préférer 1X au lieu de 1 sec")

        return {
            "match": f"{equipe_dom} vs {equipe_ext}",
            "journee": journee,
            "favori": favori,
            "choix_expert": choix_expert,
            "confiance": decision["classification"],
            "indice_confiance": decision["indice_confiance"],
            "recommandation": decision["recommandation"],
            "probabilites": {"1": round(prob_1, 1), "X": round(prob_x, 1), "2": round(prob_2, 1)},
            "modules": {
                "trajectoire_dom": traj_dom,
                "trajectoire_ext": traj_ext,
                "mss_dom": mss_dom,
                "mss_ext": mss_ext,
                "fatigue_dom": fat_dom,
                "fatigue_ext": fat_ext,
                "decision": decision
            },
            "alertes": alertes_globales
        }

    # ══════════════════════════════════════════
    #  PERFORMANCE GLOBALE (pour Tab Performance)
    # ══════════════════════════════════════════

    def calculer_performance_globale(self, season_data: dict) -> dict:
        """
        Calcule les statistiques de performance de l'Oracle sur la saison.

        Args:
            season_data : données de la saison (depuis oracle_history.json)

        Returns:
            dict avec taux de réussite, scores exacts, rating général
        """
        total, corrects_1n2, scores_exacts, points_total = 0, 0, 0, 0

        for jk, data in season_data.items():
            pronos = data.get("pro", [])
            resultats = data.get("res", [])

            for i, res in enumerate(resultats):
                if i >= len(pronos):
                    break
                total += 1
                try:
                    # Résultat réel
                    s_h, s_a = map(int, res["s"].replace("-", ":").split(":"))
                    res_reel = "1" if s_h > s_a else ("2" if s_a > s_h else "X")

                    # Prono
                    prono_txt = pronos[i].get("m", "") if isinstance(pronos[i], dict) else str(pronos[i])

                    # Vérification 1N2
                    if res_reel == "1" and equipe_dom_gagne(prono_txt):
                        corrects_1n2 += 1; points_total += 3
                    elif res_reel == "X" and "nul" in prono_txt.lower():
                        corrects_1n2 += 1; points_total += 2
                    elif res_reel == "2" and equipe_ext_gagne(prono_txt):
                        corrects_1n2 += 1; points_total += 3

                    # Vérification score exact
                    score_predit = extraire_score(prono_txt)
                    if score_predit and score_predit == (s_h, s_a):
                        scores_exacts += 1; points_total += 5

                except Exception:
                    continue

        if total == 0:
            return {"total_matchs": 0, "taux_1n2": 0, "scores_exacts": 0, "moyenne_points": 0, "rating_general": 0}

        taux_1n2 = (corrects_1n2 / total) * 100
        moyenne_points = points_total / total
        rating = min(100, (taux_1n2 * 0.6) + (scores_exacts / total * 100 * 0.3) + (moyenne_points / 5 * 10))

        return {
            "total_matchs": total,
            "taux_1n2": round(taux_1n2, 1),
            "scores_exacts": scores_exacts,
            "moyenne_points": round(moyenne_points, 2),
            "rating_general": round(rating, 1)
        }


# ─────────────────────────────────────────────
#  FONCTIONS UTILITAIRES
# ─────────────────────────────────────────────

def extraire_score(texte: str):
    """Extrait un score (x, y) depuis un texte de prono."""
    import re
    m = re.search(r"(\d+)\s*[:\-]\s*(\d+)", texte)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return None

def equipe_dom_gagne(texte: str) -> bool:
    score = extraire_score(texte)
    return score is not None and score[0] > score[1]

def equipe_ext_gagne(texte: str) -> bool:
    score = extraire_score(texte)
    return score is not None and score[1] > score[0]


# ─────────────────────────────────────────────
#  INSTANCE GLOBALE (importée par l'app principale)
# ─────────────────────────────────────────────

cerveau1 = CerveauI()


# ─────────────────────────────────────────────
#  TEST RAPIDE (exécution directe du fichier)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("   TEST CERVEAU I — Oracle Mahita")
    print("=" * 60)

    resultat = cerveau1.analyser_match(
        equipe_dom="Manchester Blue",
        equipe_ext="Brentford",
        cotes=[1.55, 3.80, 5.50],
        journee=35,
        rang_dom=2,
        rang_ext=12,
        serie_dom=3,
        serie_ext=1,
        forme_dom=["V", "V", "V", "V", "N", "V"],
        forme_ext=["D", "V", "N", "D", "V", "D"],
        match_precedent_dom="London Reds"
    )

    print(f"\nMatch    : {resultat['match']} | J{resultat['journee']}")
    print(f"Favori   : {resultat['favori']}")
    print(f"Choix    : {resultat['choix_expert']}")
    print(f"Confiance: {resultat['indice_confiance']}% — {resultat['confiance']}")
    print(f"\nAlertes :")
    for a in resultat["alertes"]:
        print(f"  {a}")
    print("\n✅ Cerveau I opérationnel.")
