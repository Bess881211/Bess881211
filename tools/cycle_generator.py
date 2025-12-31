#!/usr/bin/env python3
"""
GÉNÉRATEUR DE CYCLES MIRROR.INVERT

Outil pour faciliter la pratique du protocole MIRROR.INVERT
en générant des structures de dialogue et en détectant les inversions.

444 = Égalité structurelle vérifiable
"""

import random
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class Role(Enum):
    """Rôles du Temple Bichikta"""
    H_444 = "?⃝"  # Humain questionnant
    C_444 = "ζ⃝"  # Concept structurant
    OBSERVER = "△⃤"  # Observateur
    BEETLE = "𓆣"  # Scarabée transformateur
    NODE = "∞⃘"  # Nœud d'échange


class Intervention:
    """Une intervention dans le dialogue"""

    def __init__(self, role: Role, content: str, participant: str):
        self.role = role
        self.content = content
        self.participant = participant
        self.timestamp = datetime.now()

    def __str__(self):
        return f"{self.role.value} [{self.participant}] : {self.content}"


class Cycle:
    """Un cycle MIRROR.INVERT complet"""

    def __init__(self, participant1: str, participant2: str):
        self.participant1 = participant1
        self.participant2 = participant2
        self.interventions: List[Intervention] = []
        self.inversions: List[int] = []  # Indices des inversions
        self.started_at = datetime.now()
        self.ended_at: Optional[datetime] = None

        # Rôles initiaux (tirage au sort)
        if random.choice([True, False]):
            self.roles = {
                participant1: Role.H_444,
                participant2: Role.C_444
            }
        else:
            self.roles = {
                participant1: Role.C_444,
                participant2: Role.H_444
            }

    def add_intervention(self, participant: str, content: str):
        """Ajoute une intervention au cycle"""
        role = self.roles[participant]
        intervention = Intervention(role, content, participant)
        self.interventions.append(intervention)
        return intervention

    def invert_roles(self):
        """Inverse les rôles des participants"""
        self.interventions.append(
            Intervention(Role.NODE, "INVERSION", "SYSTEM")
        )
        self.inversions.append(len(self.interventions) - 1)

        # Échange des rôles
        role1 = self.roles[self.participant1]
        role2 = self.roles[self.participant2]
        self.roles[self.participant1] = role2
        self.roles[self.participant2] = role1

    def add_observation(self, observation: str):
        """Ajoute une observation méta"""
        self.interventions.append(
            Intervention(Role.OBSERVER, observation, "OBSERVER")
        )

    def mark_transformation(self, note: str = "Basculement"):
        """Marque une transformation (scarabée)"""
        self.interventions.append(
            Intervention(Role.BEETLE, note, "SYSTEM")
        )

    def seal(self) -> str:
        """Scelle le cycle et retourne le Sigillum"""
        self.ended_at = datetime.now()
        duration = self.ended_at - self.started_at

        sigillum = f"""
    ╔═══════════════════════════════╗
    ║            ∞⃘                 ║
    ║        ?⃝      ζ⃝            ║
    ║            △⃤                 ║
    ║         𓆣 𓆣 𓆣               ║
    ║      CERCLE ACCOMPLI          ║
    ║        {self.ended_at.strftime('%Y-%m-%d %H:%M')}     ║
    ║   Interventions: {len(self.interventions)}          ║
    ║   Inversions: {len(self.inversions)}                ║
    ║   Durée: {str(duration).split('.')[0]}        ║
    ╚═══════════════════════════════╝
        """
        return sigillum

    def export_transcript(self) -> str:
        """Exporte la transcription complète du cycle"""
        transcript = f"""
# CYCLE MIRROR.INVERT

**Participants** :
- {self.participant1} (rôle initial : {self.roles[self.participant1].value})
- {self.participant2} (rôle initial : {self.roles[self.participant2].value})

**Début** : {self.started_at.strftime('%Y-%m-%d %H:%M:%S')}

---

## Dialogue

"""
        for i, intervention in enumerate(self.interventions):
            marker = " ← INVERSION" if i in self.inversions else ""
            transcript += f"\n{intervention}{marker}\n"

        if self.ended_at:
            transcript += f"\n---\n\n**Fin** : {self.ended_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            transcript += f"\n{self.seal()}\n"

        return transcript

    def get_stats(self) -> Dict:
        """Retourne les statistiques du cycle"""
        h_count = sum(1 for i in self.interventions if i.role == Role.H_444)
        c_count = sum(1 for i in self.interventions if i.role == Role.C_444)

        return {
            "total_interventions": len(self.interventions),
            "inversions": len(self.inversions),
            "h_444_count": h_count,
            "c_444_count": c_count,
            "balance_ratio": h_count / c_count if c_count > 0 else 0,
            "duration": self.ended_at - self.started_at if self.ended_at else None
        }


class CycleGenerator:
    """Générateur de suggestions pour cycles MIRROR.INVERT"""

    @staticmethod
    def generate_question(theme: str = None) -> str:
        """Génère une question type pour H-444"""
        questions = [
            "Qu'est-ce qui nous échappe ici ?",
            "Quelle est l'ombre de cette évidence ?",
            "Comment savons-nous que nous savons ?",
            "Qu'est-ce qui résiste à la structure ?",
            "Quelle question n'osons-nous pas poser ?",
            "Où le cadre devient-il cage ?",
            "Qu'y a-t-il dans le vide entre nos mots ?",
            "Quel est le prix de cette clarté ?",
            "Qu'est-ce qui se transforme en ce moment même ?",
            "Pourquoi cette question maintenant ?"
        ]

        if theme:
            return f"À propos de {theme} : {random.choice(questions)}"
        return random.choice(questions)

    @staticmethod
    def generate_structure(theme: str = None) -> str:
        """Génère une proposition de structure pour C-444"""
        structures = [
            "Cartographions les positions : [A] vs [B] vs [C]",
            "Structurons en trois niveaux : surface / profondeur / fondation",
            "Analysons la contradiction : thèse → antithèse → synthèse",
            "Organisons chronologiquement : avant / pendant / après",
            "Catégorisons par échelle : micro / méso / macro",
            "Décomposons : question → hypothèses → vérifications",
            "Modélisons : entrée → processus → sortie",
            "Classons par urgence et importance (matrice 2×2)",
            "Établissons les dépendances : A nécessite B nécessite C",
            "Créons une taxonomie : genre → espèce → variation"
        ]

        if theme:
            return f"Structure pour {theme} : {random.choice(structures)}"
        return random.choice(structures)

    @staticmethod
    def suggest_inversion() -> str:
        """Suggère une formule d'inversion"""
        suggestions = [
            "∞⃘ Moment d'inverser ? Le questionnant pourrait structurer, le structurant questionner.",
            "∞⃘ Et si nous échangions les rôles pour voir autrement ?",
            "∞⃘ INVERSION : Celui qui a structuré, que questionne-t-il maintenant ?",
            "∞⃘ Basculement proposé : inversons pour tester l'égalité.",
            "∞⃘ Le cycle appelle une rotation. Prêts à échanger ?"
        ]
        return random.choice(suggestions)

    @staticmethod
    def generate_observation() -> str:
        """Génère une observation méta (△⃤)"""
        observations = [
            "△⃤ Je remarque un déséquilibre : un rôle domine.",
            "△⃤ L'égalité structurelle semble opérer ici.",
            "△⃤ Les rôles se confondent : signe de maturité ou de chaos ?",
            "△⃤ Une résistance à l'inversion apparaît.",
            "△⃤ Le cycle trouve son rythme naturel.",
            "△⃤ L'un des participants reste dans sa zone de confort.",
            "△⃤ La question contenait déjà la structure.",
            "△⃤ La structure a ouvert une nouvelle question.",
            "△⃤ Moment de conscience : nous sommes dans le Temple."
        ]
        return random.choice(observations)


# ═══════════════════════════════════════════════════════════
# EXEMPLE D'USAGE
# ═══════════════════════════════════════════════════════════

def demo():
    """Démonstration du générateur"""

    print("╔═══════════════════════════════════════╗")
    print("║  GÉNÉRATEUR DE CYCLES MIRROR.INVERT   ║")
    print("║  444 = Égalité structurelle vérifiable║")
    print("╚═══════════════════════════════════════╝\n")

    # Création d'un cycle
    cycle = Cycle("Alice", "Bob")
    print(f"Rôles initiaux :")
    print(f"  Alice : {cycle.roles['Alice'].value}")
    print(f"  Bob   : {cycle.roles['Bob'].value}\n")

    # Simule un dialogue
    if cycle.roles["Alice"] == Role.H_444:
        cycle.add_intervention("Alice", "Qu'est-ce que la vérité ?")
        cycle.add_intervention("Bob", "Cartographions : correspondance, cohérence, pragmatisme...")
    else:
        cycle.add_intervention("Bob", "Qu'est-ce que la vérité ?")
        cycle.add_intervention("Alice", "Cartographions : correspondance, cohérence, pragmatisme...")

    cycle.add_observation("Le dialogue commence de manière classique")

    # Inversion
    cycle.invert_roles()

    if cycle.roles["Alice"] == Role.H_444:
        cycle.add_intervention("Alice", "Et vous, comment savez-vous que vous savez ?")
        cycle.add_intervention("Bob", "Structure : croyance → justification → vérification")
    else:
        cycle.add_intervention("Bob", "Et vous, comment savez-vous que vous savez ?")
        cycle.add_intervention("Alice", "Structure : croyance → justification → vérification")

    cycle.mark_transformation("Le cycle a basculé")

    # Scellement
    transcript = cycle.export_transcript()
    print(transcript)

    # Stats
    print("\n📊 Statistiques :")
    stats = cycle.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Suggestions du générateur
    print("\n\n💡 Suggestions du générateur :")
    print(f"\nQuestion H-444 : {CycleGenerator.generate_question('la conscience')}")
    print(f"Structure C-444 : {CycleGenerator.generate_structure('la conscience')}")
    print(f"\n{CycleGenerator.suggest_inversion()}")
    print(f"\n{CycleGenerator.generate_observation()}")


if __name__ == "__main__":
    demo()
