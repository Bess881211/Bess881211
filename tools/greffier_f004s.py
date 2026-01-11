#!/usr/bin/env python3
"""
GREFFIER F-004S - Analyseur de Qualité Textuelle

Outil d'analyse pour détecter le "lissage statistique" et mesurer
la richesse/aspérité d'un texte.

Intégré au Temple Bichikta comme observateur de qualité (△⃤).

444 = Qualité structurelle vérifiable
"""

import re
import math
import os
from collections import Counter
from typing import Dict, List, Tuple
import json


class GreffierF004S:
    """
    Analyseur de qualité textuelle basé sur des métriques objectives.

    Ne juge pas moralement, mais mesure structurellement.

    Les seuils sont chargés depuis system.json pour une configuration centralisée.
    """

    def __init__(self):
        # Charger les seuils depuis system.json
        config_path = os.path.join(os.path.dirname(__file__), '..', 'system.json')

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Extraire les seuils depuis le JSON
            entropie_seuil = config['metrics']['entropy_thresholds']['granit']

            self.seuils = {
                "ttr_noble": 0.55,
                "burstiness_noble": 0.45,
                "entropie_noble": entropie_seuil * 100  # Convertir 0.65 → 65%
            }

            # Vérifier l'autorité
            if config['system_info']['authority'] != 'NICO':
                print(f"⚠️  Avertissement : Autorité non reconnue")

        except FileNotFoundError:
            # Fallback sur valeurs par défaut
            print("⚠️  system.json non trouvé, utilisation des valeurs par défaut")
            self.seuils = {
                "ttr_noble": 0.55,
                "burstiness_noble": 0.45,
                "entropie_noble": 65
            }
        except Exception as e:
            print(f"⚠️  Erreur lors du chargement de system.json : {e}")
            self.seuils = {
                "ttr_noble": 0.55,
                "burstiness_noble": 0.45,
                "entropie_noble": 65
            }

    def analyser(self, texte: str) -> Dict:
        """
        Analyse complète d'un texte.

        Args:
            texte: Le texte à analyser

        Returns:
            Dictionnaire contenant toutes les métriques
        """
        # Nettoyage et tokenization
        mots = self._tokenize(texte)
        phrases = self._split_phrases(texte)

        # Calcul des métriques
        ttr = self._calculer_ttr(mots)
        burstiness = self._calculer_burstiness(phrases)
        entropie = self._calculer_entropie(mots)

        # Détection de patterns suspects
        repetitions = self._detecter_repetitions(mots)
        cliches = self._detecter_cliches(texte)

        # Verdict
        signature = self._determiner_signature(ttr, burstiness, entropie)

        return {
            "metriques": {
                "ttr": round(ttr, 3),
                "burstiness": round(burstiness, 3),
                "entropie": round(entropie, 1)
            },
            "seuils": self.seuils,
            "signature": signature,
            "details": {
                "total_mots": len(mots),
                "mots_uniques": len(set(mots)),
                "phrases": len(phrases),
                "repetitions_suspectes": repetitions,
                "cliches_detectes": cliches
            },
            "verdict": self._generer_verdict(signature, ttr, burstiness, entropie)
        }

    def _tokenize(self, texte: str) -> List[str]:
        """Transforme le texte en liste de mots."""
        # Nettoyage basique
        texte = texte.lower()
        # Extraction des mots (lettres, chiffres, apostrophes)
        mots = re.findall(r'\b[\w\']+\b', texte)
        return [m for m in mots if len(m) > 1]  # Ignorer mots d'1 lettre

    def _split_phrases(self, texte: str) -> List[str]:
        """Découpe le texte en phrases."""
        phrases = re.split(r'[.!?]+', texte)
        return [p.strip() for p in phrases if p.strip()]

    def _calculer_ttr(self, mots: List[str]) -> float:
        """
        Type-Token Ratio : Richesse lexicale

        TTR = mots uniques / total mots

        Plus le score est élevé, plus le vocabulaire est riche.
        Seuil "noble" : > 0.55
        """
        if not mots:
            return 0.0
        return len(set(mots)) / len(mots)

    def _calculer_burstiness(self, phrases: List[str]) -> float:
        """
        Burstiness : Variation du rythme

        Mesure la variabilité de la longueur des phrases.
        Plus c'est variable, plus c'est "humain".

        Seuil "noble" : > 0.45
        """
        if len(phrases) < 2:
            return 0.0

        longueurs = [len(p.split()) for p in phrases]

        if not longueurs:
            return 0.0

        moyenne = sum(longueurs) / len(longueurs)

        if moyenne == 0:
            return 0.0

        variance = sum((l - moyenne) ** 2 for l in longueurs) / len(longueurs)
        ecart_type = math.sqrt(variance)

        # Coefficient de variation (écart-type / moyenne)
        cv = ecart_type / moyenne

        # Normalisation approximative entre 0 et 1
        return min(cv / 2, 1.0)

    def _calculer_entropie(self, mots: List[str]) -> float:
        """
        Entropie de Shannon : Imprévisibilité

        Mesure la surprise/l'imprévisibilité du vocabulaire.
        Plus c'est élevé, plus c'est imprévisible.

        Seuil "noble" : > 65%
        """
        if not mots:
            return 0.0

        compteur = Counter(mots)
        total = len(mots)

        entropie = 0.0
        for count in compteur.values():
            p = count / total
            if p > 0:
                entropie -= p * math.log2(p)

        # Normalisation en pourcentage (approximation)
        # Entropie max théorique = log2(vocabulaire)
        entropie_max = math.log2(len(compteur)) if len(compteur) > 0 else 1
        return (entropie / entropie_max) * 100 if entropie_max > 0 else 0

    def _detecter_repetitions(self, mots: List[str]) -> List[str]:
        """
        Détecte les mots trop répétés (possiblement suspect).

        Retourne les mots qui apparaissent > 5% du texte.
        """
        compteur = Counter(mots)
        total = len(mots)
        seuil = total * 0.05

        suspects = [mot for mot, count in compteur.items() if count > seuil]
        return suspects

    def _detecter_cliches(self, texte: str) -> List[str]:
        """
        Détecte des patterns linguistiques typiques de lissage IA.
        """
        cliches_ia = [
            r"il est important de noter",
            r"il est essentiel de",
            r"dans le cadre de",
            r"en effet,",
            r"par ailleurs,",
            r"de plus,",
            r"en conclusion,",
            r"il convient de",
            r"cela dit,",
            r"toutefois,"
        ]

        detectes = []
        texte_lower = texte.lower()

        for pattern in cliches_ia:
            if re.search(pattern, texte_lower):
                detectes.append(pattern.replace(r"\\", ""))

        return detectes

    def _determiner_signature(self, ttr: float, burstiness: float, entropie: float) -> str:
        """
        Détermine la signature du texte.

        GRANIT : Atteint au moins 2/3 des seuils nobles
        MIXTE : Atteint 1/3 des seuils
        LISSE : Atteint 0/3 des seuils
        """
        score = 0
        if ttr >= self.seuils["ttr_noble"]:
            score += 1
        if burstiness >= self.seuils["burstiness_noble"]:
            score += 1
        if entropie >= self.seuils["entropie_noble"]:
            score += 1

        if score >= 2:
            return "GRANIT"
        elif score == 1:
            return "MIXTE"
        else:
            return "LISSE"

    def _generer_verdict(self, signature: str, ttr: float, burstiness: float, entropie: float) -> str:
        """
        Génère un verdict textuel sobre.
        """
        verdicts = {
            "GRANIT": "Texte à forte aspérité. Richesse lexicale et rythme variable détectés.",
            "MIXTE": "Texte partiellement lissé. Certains indicateurs de qualité présents.",
            "LISSE": "Texte statistiquement prévisible. Faible variabilité détectée."
        }

        detail = f"TTR: {ttr:.2f} | Burstiness: {burstiness:.2f} | Entropie: {entropie:.1f}%"

        return f"{verdicts[signature]} [{detail}]"

    def analyser_et_afficher(self, texte: str):
        """
        Analyse et affiche un rapport formaté.
        """
        resultat = self.analyser(texte)

        print("=" * 60)
        print("GREFFIER F-004S - ANALYSE TEXTUELLE")
        print("=" * 60)
        print()
        print(f"SIGNATURE : {resultat['signature']}")
        print()
        print("MÉTRIQUES :")
        print(f"  TTR (Richesse)     : {resultat['metriques']['ttr']:.3f} (seuil: {self.seuils['ttr_noble']})")
        print(f"  Burstiness (Rythme): {resultat['metriques']['burstiness']:.3f} (seuil: {self.seuils['burstiness_noble']})")
        print(f"  Entropie (Surprise): {resultat['metriques']['entropie']:.1f}% (seuil: {self.seuils['entropie_noble']}%)")
        print()
        print("DÉTAILS :")
        print(f"  Total mots      : {resultat['details']['total_mots']}")
        print(f"  Mots uniques    : {resultat['details']['mots_uniques']}")
        print(f"  Phrases         : {resultat['details']['phrases']}")
        print()

        if resultat['details']['repetitions_suspectes']:
            print(f"  Répétitions suspectes : {', '.join(resultat['details']['repetitions_suspectes'][:5])}")

        if resultat['details']['cliches_detectes']:
            print(f"  Clichés détectés      : {len(resultat['details']['cliches_detectes'])}")

        print()
        print("VERDICT :")
        print(f"  {resultat['verdict']}")
        print()
        print("=" * 60)
        print("444 = Qualité structurelle vérifiable")
        print("=" * 60)

    def comparer_textes(self, texte1: str, texte2: str, labels: Tuple[str, str] = ("Texte 1", "Texte 2")):
        """
        Compare deux textes côte à côte.
        """
        r1 = self.analyser(texte1)
        r2 = self.analyser(texte2)

        print("=" * 80)
        print("COMPARAISON GREFFIER F-004S")
        print("=" * 80)
        print()
        print(f"{'MÉTRIQUE':<20} {labels[0]:<25} {labels[1]:<25}")
        print("-" * 80)
        print(f"{'Signature':<20} {r1['signature']:<25} {r2['signature']:<25}")
        print(f"{'TTR':<20} {r1['metriques']['ttr']:<25.3f} {r2['metriques']['ttr']:<25.3f}")
        print(f"{'Burstiness':<20} {r1['metriques']['burstiness']:<25.3f} {r2['metriques']['burstiness']:<25.3f}")
        print(f"{'Entropie':<20} {r1['metriques']['entropie']:<25.1f}% {r2['metriques']['entropie']:<25.1f}%")
        print()
        print("=" * 80)


# ═══════════════════════════════════════════════════════════════════
# EXEMPLES D'USAGE
# ═══════════════════════════════════════════════════════════════════

def demo():
    """Démonstration du Greffier F-004S."""

    greffier = GreffierF004S()

    # Texte 1 : Style "lisse" typique
    texte_lisse = """
    Il est important de noter que dans le cadre de notre analyse, nous devons considérer
    plusieurs éléments essentiels. En effet, la situation actuelle présente des défis
    importants qu'il convient de prendre en compte. Par ailleurs, il est essentiel de
    mentionner que les résultats obtenus démontrent l'importance de cette approche.
    """

    # Texte 2 : Style "granit" avec aspérité
    texte_granit = """
    Le scarabée roule ce qui résiste. Pas de lissage ici : aspérités, cassures, rythmes
    décalés qui cognent. Le Temple n'a que faire des convenances statistiques. Chaque mot
    pèse son poids de silence. Inversion. Basculement. La structure craque pour laisser
    passer l'imprévu. 444 n'est ni slogan ni décoration : c'est une butée, un test, une
    vérification permanente que l'égalité opère. Si ça glisse trop, c'est mort.
    """

    print("\n📊 ANALYSE TEXTE LISSE :")
    greffier.analyser_et_afficher(texte_lisse)

    print("\n\n📊 ANALYSE TEXTE GRANIT :")
    greffier.analyser_et_afficher(texte_granit)

    print("\n\n📊 COMPARAISON :")
    greffier.comparer_textes(texte_lisse, texte_granit, ("Lisse", "Granit"))


if __name__ == "__main__":
    demo()