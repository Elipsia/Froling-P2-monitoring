# Froling P2 Monitoring — Supervision en français d'une chaudière Fröling P2 (Lambdatronic S3100)

Module de supervision **entièrement en français** pour une chaudière à granulés **Fröling P2** (2006) équipée de la régulation **Lambdatronic S3100**.

Il s'agit d'une adaptation francisée de l'excellente intégration [ha-froeling-s3100](https://github.com/Alexander423/ha-froeling-s3100) d'Alexander Hechnet (MIT), elle-même basée sur l'analyse du protocole série de la S3100 réalisée par [dhoepfl/Radiator](https://github.com/dhoepfl/Radiator).

## Ce que vous obtenez

- **Températures** : chaudière, fumées, chambre de combustion, ballon (haut/milieu/bas), eau chaude sanitaire, extérieure, départs des circuits de chauffage (réel + consigne), retour
- **États et commandes** : mode de fonctionnement, ventilateur de tirage, air primaire/secondaire, vis d'alimentation, % oxygène résiduel, niveau de pellets, pompes
- **Compteurs** : heures de fonctionnement, démarrages du brûleur, heures de maintien du feu
- **Messages d'erreur** : événement en temps réel dès qu'un défaut apparaît (trame M3), traduits en français, avec historique
- **Paramètres** : tous les paramètres du menu client visibles ; modification à distance possible (option expérimentale, désactivée par défaut)
- **Sur téléphone** : application Home Assistant (iOS/Android) avec notifications push en cas d'erreur, historique et graphiques

⚠️ **Important** : les chaudières récentes (Lambdatronic S3200) utilisent Modbus et **ne sont pas concernées**. La P2 de 2006 parle un protocole série propriétaire sur son connecteur de service.

## Matériel nécessaire

| Élément | Exemple | Prix approx. |
|---|---|---|
| Raspberry Pi (3/4/5, 4 Go de RAM recommandés) + carte microSD + alimentation | — | 50–90 € |
| Convertisseur RS232 ↔ Ethernet/Wi-Fi (serveur TCP transparent) | Waveshare RS232 to ETH (B), ou USR-W630 pour le Wi-Fi | 20–35 € |
| Câble RS232 DB9 mâle-mâle croisé (« null modem ») — voir « Câblage » selon votre connecteur | câble null modem | 8–15 € |

Le convertisseur Waveshare est recommandé car c'est la configuration testée par l'intégration. Il se configure (via son utilitaire) en **serveur TCP, port 4196, 9600 bauds, 8N1**.

Alternative possible : un simple adaptateur USB↔RS232 branché sur le Raspberry Pi, avec un pont série vers TCP (ser2net) — mais cela nécessite une configuration supplémentaire.

## Câblage

⚠️ **Coupez l'alimentation de la chaudière au disjoncteur avant tout raccordement.** Rester en lecture seule ne modifie rien au fonctionnement de la chaudière : le port de service est conçu pour la visualisation.

Le port « Bedien-Erweiterung » de la Lambdatronic 3100 existe en **deux variantes matérielles** selon la révision. Identifiez la vôtre (coupez le courant et ouvrez le caisson de régulation au préalable) :

### Variante A — prise DB9 femelle 9 trous

1. Localisez la prise DB9 femelle (9 trous, format port série de PC) sur la carte de la régulation.
2. Reliez-la au convertisseur avec le câble null modem (TXD/RXD croisés, GND commun).

### Variante B — connecteur 4 broches (+US / TXD / RXD / GND)

Une prise plastique à 4 trous, femelle (pas 2,54 mm type Molex, étiquettes imprimées sur la carte). La prise étant à trous, il faut des **broches mâles** au bout des fils : le câblage se fait avec des câbles Dupont **mâle**-bout dénudé et un connecteur DB9 à bornier. Vérifiez au préalable l'écart entre deux trous adjacents : ~2,54 mm = standard Dupont ; ~3,96 mm = il faudra un connecteur Molex KK mâle 3,96 mm avec embases à souder.

| Broche P3100 | → | Broche DB9 mâle | → | câble null modem → convertisseur |
|---|---|---|---|---|
| TXD (la chaudière parle) | → | broche 3 | → | le câble croise vers RX |
| RXD (la chaudière écoute) | → | broche 2 | → | le câble croise vers TX |
| GND | → | broche 5 | → | masse |
| +US | → | **non branchée** — isolez la fiche (chatterton/gaine thermo) | |

Matériel pour cette variante : connecteur DB9 à bornier à vis (~5 €) + câbles Dupont **mâle**-mâle (~5 €, on coupe une extrémité pour le dénuder côté DB9) + gaine thermo pour isoler la broche +US non branchée.

**Diagnostic** : si l'intégration affiche « La S3100 ne répond pas » alors que le convertisseur est joignable, intervertissez les fils TXD et RXD — un câblage inversé ne casse rien, la chaudière reste simplement muette.

### Dans tous les cas

1. Configurez le convertisseur : serveur TCP, port 4196, 9600 bauds, 8 bits, pas de parité, 1 bit de stop.
2. Branchez le convertisseur sur votre réseau local (Ethernet, Wi-Fi ou CPL — réservez-lui une IP fixe).
3. Remettez la chaudière sous tension : la LED d'état doit rester verte.

**Remarque** : la Fröling P2 de 2006 est équipée de la **Lambdatronic P 3100** (version pellets de la plateforme Lambdatronic 3100 — le « P » remplace le « S » selon le type de chaudière). Carte, firmware, port série et protocole sont identiques : cette intégration fonctionne telle quelle.

## Installation

### 1. Home Assistant

Installez [Home Assistant OS](https://www.home-assistant.io/installation/) sur le Raspberry Pi, puis l'application **Home Assistant Companion** sur votre téléphone. Mettez l'interface en français : Profil → Langue → Français (l'intégration affichera alors tous les libellés en français).

### 2. L'intégration

Via HACS (recommandé) :
1. Ajoutez ce dépôt dans HACS → Intégrations → ⋮ → Dépôts personnalisés : `https://github.com/Elipsia/Froling-P2-monitoring`, catégorie « Intégration ».
2. Recherchez « Fröling Lambdatronic S3100 » et installez.
3. Redémarrez Home Assistant.

Ou manuellement : copiez le dossier `custom_components/froeling_s3100` dans `/config/custom_components/` de Home Assistant, puis redémarrez.

### 3. Configuration

1. Paramètres → Appareils et services → Ajouter une intégration → **Fröling Lambdatronic S3100**.
2. Saisissez l'adresse IP du convertisseur RS232↔Ethernet et son port (4196 par défaut).
3. La chaudière est détectée : toutes les sondes, états et paramètres apparaissent, en français.

## Notifications d'erreur sur le téléphone

Créez une automatisation dans Home Assistant :

```yaml
alias: Erreur chaudière Fröling
description: Notifie quand la chaudière Fröling signale un défaut
triggers:
  - trigger: event
    event_type: fault
actions:
  - action: persistent_notification.create
    data:
      title: "⚠️ Défaut chaudière Fröling (erreur {{ trigger.event.data.error_id }})"
      message: >-
        {{ trigger.event.data.text }}
        (message d'origine : {{ trigger.event.data.text_origin }})
        à {{ trigger.event.data.controller_time }}
  # En production, ajoutez aussi une notification mobile : 
  # - action: notify.mobile_app_mon_telephone
  #   data:
  #     title: "⚠️ Défaut chaudière Fröling"
  #     message: "{{ trigger.event.data.text }}"
```

L'entité événement `event.froling_s3100_message_d_erreur` émet un événement bus de type `fault` à chaque défaut (données : `text` traduit, `error_id`, `state`, `controller_time`...). Adaptez l'identifiant si votre entité a un autre identifiant

Chaque message d'erreur envoyé par la chaudière (en allemand) est automatiquement traduit en français via la table `custom_components/froeling_s3100/fault_texts_fr.py`. Si un message n'est pas encore répertorié, il s'affiche sous la forme « Texte inconnu (... » : signalez-le dans les issues et complétez la table — toute contribution est bienvenue.

Les **valeurs textuelles** (modes de fonctionnement « Winterbetrieb », états « Heizen », « Betriebsbereit »...) sont également traduites en français à l'affichage via `custom_components/froeling_s3100/value_texts_fr.py` (« Mode hiver », « En chauffe », « Prêt »...). Les valeurs brutes restent en allemand en interne — les capteurs dérivés (Feu actif, Défaut) continuent de fonctionner sur les textes d'origine. Une valeur non répertoriée s'affiche telle quelle : complétez la table de la même façon.

## Vue graphique de la chaudière

Deux approches sont fournies :

### 1. Visuels détaillés par composant (recommandé)

Le dossier `www/froeling/` contient des schémas SVG professionnels de la chaudière, du ballon ECS, des circuits de chauffage et de l'extraction de granulés — adaptés avec l'accord de leur auteur (licence MIT) depuis [GyroGearl00se/ESPHome-Froeling-Lambdatronic_3200](https://github.com/GyroGearl00se/ESPHome-Froeling-Lambdatronic_3200), avec les identifiants d'entités remappés vers cette intégration. Les valeurs s'affichent **dans** le dessin (températures, %, niveau de pellets) et les composants **changent de couleur** selon leur état (chauffage actif en rouge/orange, pompes en vert) grâce à la carte « Floorplan ».

Installation :

1. Installez la carte **Floorplan Card** via HACS (recherchez « Floorplan »).
2. Copiez le dossier `www/froeling/` dans `/config/www/froeling/` de Home Assistant.
3. Créez un tableau de bord en mode YAML et collez le contenu de [`ha_dashboard_froling_s3100.yaml`](ha_dashboard_froling_s3100.yaml) : cinq vues (Chaudière, Ballon ECS, Circuit 1, Circuit 2, Extraction pellets) avec les valeurs injectées dans les schémas et les listes d'entités en français.
4. Adaptez les identifiants d'entités à votre installation (Outils de développement → États) ; retirez les lignes des sondes absentes de votre configuration (par ex. le circuit 2 s'il n'existe pas).

Les schémas s'éditent avec [Inkscape](https://inkscape.org/) : les éléments Texte portent l'identifiant de l'entité qu'ils affichent (ex. `sensor.froling_s3100_temperature_chaudiere`).

### 2. Schéma d'ensemble simple (alternative)

Le fichier `www/froeling-p2.svg` est un schéma d'ensemble de la P2 (chaudière reliée directement au ballon ECS puis aux circuits, sans ballon tampon). Il s'affiche avec la carte native « Éléments d'image » (picture-elements), les valeurs étant superposées :

1. Copiez `www/froeling-p2.svg` dans `/config/www/` de Home Assistant. Le fichier devient accessible à l'adresse `/local/froeling-p2.svg`.
2. Dans un tableau de bord : **Ajouter une carte → Éléments d'image** (picture-elements), puis en mode YAML :

```yaml
type: picture-elements
image: /local/froeling-p2.svg
elements:
  - type: state-label
    entity: sensor.froling_s3100_temperature_exterieure
    style:
      top: 15%
      left: 8%
  - type: state-label
    entity: sensor.froling_s3100_temperature_des_fumees
    style:
      top: 22%
      left: 27%
  - type: state-label
    entity: sensor.froling_s3100_temperature_chaudiere
    style:
      top: 47%
      left: 21%
  - type: state-label
    entity: sensor.froling_s3100_temperature_eau_chaude_sanitaire
    style:
      top: 48%
      left: 56%
  - type: state-label
    entity: sensor.froling_s3100_niveau_de_pellets
    style:
      top: 50%
      left: 89%
  - type: state-label
    entity: sensor.froling_s3100_temperature_depart_circuit_1
    style:
      top: 43%
      left: 81%
  - type: state-label
    entity: sensor.froling_s3100_temperature_depart_circuit_2
    style:
      top: 65%
      left: 81%
```

Les identifiants d'entités sont à adapter à votre installation (Outils de développement → États). Les positions (`top`/`left` en pourcentage) sont calées sur le schéma fourni — ajustez-les si vous dessinez votre propre SVG. Pour un rendu plus soigné, la carte peut être complétée par l'extension [card-mod](https://github.com/thomasloven/lovelace-card-mod) (arrière-plan des étiquettes, arrondi) ou par des `state-icon` (icônes cliquables).

Le SVG est modifiable avec [Inkscape](https://inkscape.org/) (gratuit) : ajoutez vos propres zones (sondes KTY, pompes, vis d'alimentation...) en respectant les positions des étiquettes.

## Tableau de bord mobile

Exemple de dashboard (Paramètres → Tableaux de bord → Ajouter un tableau de bord) :

```yaml
views:
  - title: Chaudière
    type: sections
    sections:
      - type: grid
        cards:
          - type: heading
            heading: État
          - type: tile
            entity: binary_sensor.froeling_defaut
            color: red
          - type: tile
            entity: sensor.froeling_mode_de_fonctionnement
          - type: heading
            heading: Températures
          - type: tile
            entity: sensor.froeling_temperature_chaudiere
          - type: tile
            entity: sensor.froeling_temperature_des_fumees
          - type: tile
            entity: sensor.froeling_temperature_ballon_haut
          - type: tile
            entity: sensor.froeling_temperature_ballon_bas
          - type: tile
            entity: sensor.froeling_temperature_eau_chaude_sanitaire
          - type: heading
            heading: Granulés
          - type: tile
            entity: sensor.froeling_niveau_de_pellets
          - type: tile
            entity: sensor.froeling_derniere_erreur
```

Les identifiants exacts (`entity_id`) dépendent de votre installation ; vérifiez-les dans Paramètres → Appareils et services → Fröling.

## Modifier des paramètres à distance (optionnel, expérimental)

Dans les options de l'intégration, activez « Autoriser la modification des paramètres ». Les paramètres du menu client (consignes de température, horaires, ...) deviennent modifiables. **Vérifiez toujours l'affichage de la chaudière après chaque modification** : l'écriture n'a pas été validée sur toutes les versions de régulateur. Cette option est désactivée par défaut.

## Tester sans matériel (100 % virtuel)

Aucun besoin de chaudière ni de matériel pour valider le fonctionnement. Le projet embarque un **simulateur complet de la Lambdatronic S3100** qui rejoue une capture réelle (login, catalogue, mesures chaque seconde, erreurs) et se comporte exactement comme le régulateur sur le réseau :

```bash
pip install -e .
python tools/demo_virtuel.py
```

Le script démarre une S3100 virtuelle en local (TCP), s'y connecte avec le vrai client du module, affiche les 35 mesures décodées, puis injecte une erreur (trame M3) et montre sa traduction française. Vous pouvez aussi lancer le simulateur seul (`python -m froeling_s3100.simulator tests/fixtures/s3100_capture.jsonl --port 4196`) et pointer Home Assistant dessus pour valider toute l'installation avant de toucher à la chaudière.

Pour déclencher une erreur de test pendant que le simulateur tourne (par exemple pour tester une automatisation de notification dans Home Assistant) :

```bash
python tools/inject_erreur.py --port 4196 --erreur 1   # 0 = STB déclenché, 1 = sonde chaudière défectueuse
```

L'erreur est diffusée à tous les clients connectés (dont Home Assistant), exactement comme un vrai défaut de la chaudière.

**Sécurité** : par défaut, le module fonctionne en lecture seule (login « client »). La chaudière est conçue pour être interrogée par son port de visualisation ; la lecture ne modifie aucun réglage. La modification de paramètres, seule fonction à risque, est désactivée par défaut et clairement signalée comme expérimentale.

## Développement

```bash
pip install -e ".[dev]"
pytest tests/lib
```

- `custom_components/froeling_s3100/s3100/` : client du protocole série S3100 (login, trames M1/M2/M3/MA–MU, checksum, CP850)
- `custom_components/froeling_s3100/measurements.py` : correspondance entre les noms de sondes allemands annoncés par la chaudière et les entités
- `custom_components/froeling_s3100/fault_texts_fr.py` : traduction française des messages d'erreur
- `custom_components/froeling_s3100/translations/fr.json` : interface en français
- `tools/s3100_capture.py` : capture du trafic série réel pour l'analyse

## Remerciements et licences

- [Alexander423/ha-froeling-s3100](https://github.com/Alexander423/ha-froeling-s3100) — MIT — intégration Home Assistant S3100 dont ce projet est issu
- [dhoepfl/Radiator](https://github.com/dhoepfl/Radiator) — MIT — rétro-ingénierie de référence du protocole série de la Lambdatronic S3100
- [Thread mikrocontroller.net](https://www.mikrocontroller.net/topic/319990) — analyse communautaire initiale du protocole

Ce projet n'est affilié ni à Fröling ni à aucun fournisseur de matériel de chauffage. Utilisation à vos risques et périls.
