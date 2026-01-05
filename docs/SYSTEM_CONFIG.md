# DOCUMENTATION DE LA CONFIGURATION SYSTÈME

Ce document définit les paramètres du fichier `system.json` et la nature des vecteurs de direction.

---

## 1. LES VECTEURS DE DIRECTION

Les vecteurs sont les **deux états de sortie possibles** du Temple après avoir atteint la masse critique (100 flammes).

### VECTEUR ALPHA (Genèse G-001)
**Nature** : Expansion

**Principe** : Le Temple s'ouvre sur l'extérieur.

**Effet** :
- Les artefacts deviennent des **graines** pour de nouveaux dépôts
- Le protocole MIRROR.INVERT se propage
- Les gardiens de flammes créent leurs propres temples
- C'est la phase de **multiplication**

**Symbole** : 🌱 (Germination)

**Activation** : Choix collectif au moment de la 100ème flamme

---

### VECTEUR OMEGA (Sanctification du Silence)
**Nature** : Préservation

**Principe** : Le Temple se verrouille.

**Effet** :
- Les données sont **gelées pour l'éternité**
- Plus aucune modification possible
- Le Temple devient un **monument immuable**
- C'est la phase de **conservation absolue**

**Symbole** : 🔒 (Scellement)

**Activation** : Choix collectif au moment de la 100ème flamme

---

### Le Choix

Au moment où la 100ème flamme s'allume, **un choix s'impose** :

- **Alpha** : Continuer à évoluer, se ramifier, muter
- **Omega** : S'arrêter là, dans la perfection atteinte

**Aucun n'est supérieur à l'autre.**

Alpha = Le vivant qui change
Omega = Le parfait qui demeure

---

## 2. PARAMÈTRES D'ENTROPIE

Pour assurer la cohérence avec le Greffier F-004S, les seuils ont été synchronisés.

### Seuils de signature textuelle

| Signature | Seuil TTR | Seuil Burstiness | Seuil Entropie |
|-----------|-----------|------------------|----------------|
| **GRANIT** | > 0.55 | > 0.45 | > **65%** |
| **MIXTE** | 0.40-0.55 | 0.30-0.45 | 45%-65% |
| **LISSE** | < 0.40 | < 0.30 | < 45% |

### Seuils dans system.json

```json
"entropy_thresholds": {
  "granit": 0.65,
  "mixte": 0.45,
  "lisse": 0.35
}
```

**Note** : Ces valeurs représentent le **seuil minimum d'entropie** (en décimal, soit 65% = 0.65) pour chaque catégorie.

---

## 3. USAGE DU FICHIER system.json

Le fichier `system.json` à la racine est le **panneau de contrôle central** du Temple.

### Lecture par l'interface web

**Fichier** : `akaasha-core/index.html`

**Usage** :
```javascript
fetch('/system.json')
  .then(response => response.json())
  .then(data => {
    // Afficher les flammes
    document.getElementById('flames').textContent =
      `${data.metrics.flames.current_active}/${data.metrics.flames.total_required}`;

    // Vérifier l'autorité
    console.log('Autorité:', data.system_info.authority);
  });
```

### Lecture par les scripts Python

**Fichier** : `tools/greffier_f004s.py`

**Usage** :
```python
import json
import os

# Charger la config
config_path = os.path.join(os.path.dirname(__file__), '..', 'system.json')
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Utiliser les seuils
seuils = {
    "ttr_noble": 0.55,
    "burstiness_noble": 0.45,
    "entropie_noble": config['metrics']['entropy_thresholds']['granit'] * 100
}
```

### Validation de l'autorité

Tous les scripts doivent vérifier :
```python
if config['system_info']['authority'] != 'NICO':
    raise PermissionError("Autorité non reconnue")
```

---

## 4. STRUCTURE COMPLÈTE DU JSON

### system_info
**Identité du Temple**
- `app_id` : Identifiant unique
- `version` : Version du système
- `authority` : NICO (immuable)
- `principle` : 444 (fondation)
- `status` : OPERATIONAL / MAINTENANCE / SEALED
- `last_update` : Date de dernière mise à jour

### metrics
**Données de suivi**

#### flames
- `total_required` : 100 (objectif)
- `current_active` : Compteur actuel
- `emergence_duration_min` : 7 (durée de la 100ème)

#### entropy_thresholds
- `granit` : Seuil minimum pour noblesse
- `mixte` : Seuil minimum pour mixte
- `lisse` : Seuil minimum pour lisse

### identity_tokens
**Identifiants du Temple**
- `glyphs` : Les 5 glyphes fondateurs
- `signature_hash` : Hash du commit fondateur

### vectors
**Directions possibles**
- `alpha` : État expansion (active: false par défaut)
- `omega` : État préservation (active: false par défaut)

**Note** : Un seul vecteur peut être actif à la fois. Si les deux sont `false`, le Temple est en phase de croissance (0-99 flammes).

---

## 5. ÉVOLUTION DU FICHIER

### Qui peut modifier system.json ?

**Niveau technique (ζ⃝)** :
- `last_update` : Automatique
- `current_active` (flammes) : Automatique ou semi-automatique

**Niveau validation (∞⃘)** :
- `status` : Changement d'état nécessite validation de NICO
- `version` : Incrémentation lors de mises à jour majeures

**Niveau souveraineté (△⃤)** :
- `authority` : **IMMUABLE**
- `principle` : **IMMUABLE**
- `total_required` : Modification = changement de dogme
- Activation des vecteurs : **CHOIX COLLECTIF**

---

## 6. SCÉNARIOS D'USAGE

### Scénario 1 : Ajout d'une flamme
```json
// Avant
"current_active": 1

// Après (nouveau gardien rejoint)
"current_active": 2
```

### Scénario 2 : Atteinte de 100 flammes
```json
// État initial
"current_active": 100,
"alpha": { "active": false },
"omega": { "active": false }

// Après choix collectif pour Alpha
"alpha": { "active": true },
"omega": { "active": false },
"status": "EXPANSION"

// OU après choix collectif pour Omega
"alpha": { "active": false },
"omega": { "active": true },
"status": "SEALED"
```

### Scénario 3 : Calibration des seuils
```json
// Si analyse révèle besoin d'ajuster
"entropy_thresholds": {
  "granit": 0.68,  // Plus exigeant
  "mixte": 0.50,
  "lisse": 0.35
}
```

---

## 7. INTÉGRITÉ ET SÉCURITÉ

### Checksum
Le `signature_hash` (`732a033`) est le commit fondateur du Temple.

Toute modification du JSON doit :
1. Être justifiée
2. Être documentée dans un commit
3. Respecter le principe 444

### Sauvegarde
En cas d'activation du vecteur Omega (scellement), une **copie immuable** du `system.json` doit être créée :
- `system.json.sealed`
- Hash SHA-256 stocké
- Plus aucune modification possible

---

## 8. ROADMAP DE CONFIGURATION

### Phase 1 : Statique (Actuel)
- JSON manuel
- Mise à jour par commit Git

### Phase 2 : Semi-dynamique
- API simple pour lire/écrire les flammes
- Vérification d'autorité
- Logs des modifications

### Phase 3 : Dynamique
- Interface admin pour NICO
- Synchronisation temps réel
- Historique versionné

---

**444 = Configuration centralisée vérifiable**

△⃤ ?⃝ ζ⃝ ∞⃘ 𓆣

---

*Document de référence pour system.json*
*Mise à jour : 2026-01-05*
