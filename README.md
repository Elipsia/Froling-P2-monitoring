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
| Raspberry Pi (3/4/5) + carte microSD + alimentation | — | 50–90 € |
| Convertisseur RS232 ↔ Ethernet (serveur TCP transparent) | Waveshare RS232 to ETH (B) | 20–30 € |
| Câble RS232 DB9 mâle-mâle croisé (« null modem ») | câble null modem | 8–15 € |

Le convertisseur Waveshare est recommandé car c'est la configuration testée par l'intégration. Il se configure (via son utilitaire) en **serveur TCP, port 4196, 9600 bauds, 8N1**.

Alternative possible : un simple adaptateur USB↔RS232 branché sur le Raspberry Pi, avec un pont série vers TCP (ser2net) — mais cela nécessite une configuration supplémentaire.

## Câblage

1. Localisez le connecteur de service RS232 (DB9) de la Lambdatronic S3100 (connecteur « Bedien-Erweiterung », à l'arrière de la régulation).
2. Reliez-le au convertisseur avec le câble null modem (TXD/RXD croisés, GND commun).
3. Configurez le convertisseur : serveur TCP, port 4196, 9600 bauds, 8 bits, pas de parité, 1 bit de stop.
4. Branchez le convertisseur sur votre réseau local (DHCP ou IP fixe).
5. **Rester en lecture seule ne modifie rien au fonctionnement de la chaudière** ; le port est conçu pour la visualisation.

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
  - trigger: event.received
    target:
      entity_id: event.froling_s3100_message_d_erreur
    options:
      event_type:
        - fault
actions:
  - action: persistent_notification.create
    data:
      title: "⚠️ Défaut chaudière Fröling"
      message: "{{ trigger.data.text }}"
  # En production, ajoutez aussi une notification mobile : 
  # - action: notify.mobile_app_mon_telephone
  #   data:
  #     title: "⚠️ Défaut chaudière Fröling"
  #     message: "{{ trigger.data.text }}"
```

Le déclencheur `event.received` (dans l'éditeur visuel : « Événement reçu ») est le déclencheur officiel des entités d'événement : il se déclenche à chaque message d'erreur, même si l'entité ne change pas d'état. Adaptez l'identifiant `event.froling_s3100_message_d_erreur` si votre entité a un autre identifiant (Paramètres → Appareils et services → Fröling → « Message d'erreur »).

Chaque message d'erreur envoyé par la chaudière (en allemand) est automatiquement traduit en français via la table `custom_components/froeling_s3100/fault_texts_fr.py`. Si un message n'est pas encore répertorié, il s'affiche sous la forme « Texte inconnu (... » : signalez-le dans les issues et complétez la table — toute contribution est bienvenue.

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
