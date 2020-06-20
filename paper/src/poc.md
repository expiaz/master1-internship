
### Intégration

Mirage est un "*framework offensif pour l'audit des protocoles sans fil*"^[https://homepages.laas.fr/rcayre/mirage-documentation/index.html]. Il a ete pense pour le *pentest* (audit de sécurité) donc un usage exclusivement en ligne de commandes (*CLI*). Meme si le framework se veut beaucoup plus modulaire et extensible que ces predecesseurs (BTLEJack notamment), cette modularite a ete pensee pour l'interface en ligne de commandes.  
Mirage fournit des briques logicielles pour communiquer avec des appareils (dongles, sniffers) ainsi que decortiquer les protocoles, ce qui constitue le coeur du framework. Ces briques logicielles de base sont utilisees par des *modules* dans un but precis, par exemple realiser le brouillage d'une communication BLE. Mirage fournie un certain nombre de modules fournissant les attaques retrouvees dans les autres outils d'audit du BLE (*BTLEJack*, *GATTAcker*, ...) precedement discutes. Similaire a la philosophie d'Unix, ces modules sont specialisés dans une tache precise et peuvent etres assemblés entre eux pour realise des fonctionnalites plus complexes comme la connexion avec le module *ble_connect* puis l'extraction d'informations avec *ble_discover*. Enfin, il est possible de modifier les etapes d'une attaque via les *scénarios*: chaque module accepte un scénario surchargeant son flux d'execution et ses methodes.


mirage extensible certes mais seulement en CLI selon ces regles
Pas pense pour vivre dans un back-end, fait pour le pentest: une attaque puis shutdown => etat instable apres une attaque, non fiabilite des appareils utilises pour conduire l'attaque car fermeture des connexions non effectué normalement fait par shutdown de mirage
Creation API pour integration avec Flask mais couches CLI et Modules fortements liées, problemes de personnalisations de l'API sans modifier le coeur des modules ou de mirage => instanciation manuelle de l'app et des modules au besoin

### Interfaces

Inutile et long de reconduire l'interface CLI de mirage en API pour le back, la rendre accessible depuis GUI via websockets puis la rendre en HTML/CSS/JS. Les attaques selectionnees demandent actions utilisateurs car modification a la volee d'informations, seul le scan et localisation sont autonomes. Decision de laisse le front pour demo localisation et scan pour sensibilisation fuite d'informations passive BLE (smartphones, airpods, pc).  
Utilisation CLI Mirage avec modules personnalisés pour conduire les attaques choisies (et meme plus puisque mirage dispose d'une multitudes d'attaques).

# Travail realise

## Scan et localisation

1. comment trouver ?
ble_sniff, scan 3 canaux d'annonces => devices
ble_sniff scan 37 canaux de donnees => connections
PB connexions pe long, tres long car jeux chat et souris, possible para (mirage para les annonces avec 3 btlejack) sur x canaux donnees pour accelerer

2. Comment calculer ?
RSSI => peu reliable, necessite un calibrage, path-loss, dead-reckoning
TOA => necessaire de controller appareil emetteur, ici attaque donc impossible

fingerprinting => liste d'appareils et leurs positions connues, impossible dans attaque
trilateration => necessite points de donnes (parrallele GPS)
AOA/AOD => necessite materiel adequat et BLE 5.1
=> triangulation ou AOA+TOA/RSSI

3. comment integrer ? ble_locate
facon de faire de mirage avec module CLI, cleanup des threads/fifo entre scan device et connections
extension du ble_sniff et device btlejack pour integrer mes changements: but ne pas modifer le firmware car la recompilation demande une environnement precis et complexe a mettre en place.

4. GUI

## MITM

## Hijack

## Tests et validation

Connexion factice car aucun appareil BLE (coronavirus modification du sujet)


<!--

## Fonctionnalités

La preuve de concept devra fournir plusieurs fonctionnalités offensive décritent ci-après.

### Repérage

Inventaire des appareils et connexions BLE à proximité.

- Écoute des annonces sur les 3 canaux publicitaires pour récupérer les appareils émetteurs.
- Écoute des communications sur les 37 canaux de données pour répertorier celles active.

### Localisation

Localisation des appareils BLE alentours.

- Écoute passive des annonces pour extraire le calibrage du signal et calculer la distance à partir de la puissance du signal reçu.
- Si le calibrage n'est pas émit dans l'annonce, établissment d'une connexion pour récuperer la valeur si disponible.

Opération répétables autant de fois que voulu pour améliorer la précision de la localisation (minimum 3 mesures pour une position).

### Identification

Connexion directe à un appareil via son adresse bluetooth pour extraire toutes les données exposées.

- Écoute optionnelle des annonces pour identifier un esclave cible.
- Requête de connexion à la cible en tant que maître.
- Récupération des informations standardisées (GAP/GATT) ainsi que services et attributs propriétaires.

### Interception

Interception de communications et possible déchiffrement des trames.

- Écoute des communications sur les 37 canaux de données.
- Récupération de l'adresse d'accès et des paramètres d'appairage (carte des canaux, temps et nombre de sauts, etc).
- Synchronisation avec la communication et écoute des trames.
- Si la communication est chiffrée et la phase d'appairage passée, déconnexion des appareils via brouillage des communication jusqu'au temps mort.
- Écoute des canaux d'annonce: attente d'un appairage en supposant qu'il provienne des appareils precedement déconnectés.
- Récupération des informations cryptographique pour déchiffrer la connexion seulement si celle-ci n'utilise pas une clef a long terme deja établie ou une connexion securisée (BLE 4.2).
- Écoute des communications et déchiffrement des trames à la volée.

### Modification

Attaque *man in the middle* par clonage et usurpation d'un appareil BLE pour modifier les données echangées.

- Écoute passive des annonces de l'esclave cible de l'usurpation pour retransmission ultérieur et récupération de l'adresse bluetooth.
- Connexion à l'esclave cible d'usurpation pour qu'il n'émette plus d'annonces.
- Changement de l'adresse de l'usurpateur en celle de l'esclave usurpé et réémission des annonces précédement capturées.
- Attente de la connexion du maître.
- Appairage entre l'usurpateur et le maître.
- Retransmission des communications entre le maître et l'esclave par l'usurpateur.

Il sera par la suite envisageable d'associer plusieurs fonctionnalités pour réaliser des scénarios différents. Ce peut être par exemple l'usurpation d'un appareil suite au brouillage lors de l'interception des communications entre 2 appareils.

## Architecture

Le système se compose d'un front-end fournissant une interface utilisateur affichant les appareils BLE et les actions possible ainsi qu'un back-end permettant la réalisation des actions implementées.  
Le back-end se compose d'un service web (en violet sur @fig:poc-arch) pour communiquer avec le front-end, il transmet les requêtes au serveur (en rouge) qui se base sur un framework BLE offensif (en bleu) pour les traiter. Le framwork BLE offensif utilise plusieurs appareils BLE (en vert) pour mener à bien les attaques.  
Le serveur orchestre les attaques même si il ne les implémentent pas lui-même.

![Architecture du système](img/poc-architecture.png){#fig:poc-arch-2 width=85%}

## Interface

On retrouve la carte des appareils et connexions identifiés avec leur distance et position estimée par rapport au système (voir @fig:poc-ui: zone rouge *Scan*).  

Pour chaque cible (appareil ou connexion), des attaques sont disponibles:
- Récupération du profil ou modification des transimissions par usurpation pour un appareil BLE emettant des annonces (zone bleue *Devices*).
- Déconnexion des appareils ou interception des communications entre deux appareils appairés (zone bleue *Connections*).

Une troisieme section permet de suivre le déroulement de l'attaque chosie (zone verte *Action progress*). Celle-ci est découpée en phases, dès que la phase courante est terminée sans erreur (carré vert), la phase suivante est exécutée. Lorsqu'une phase échoue l'attaque s'arrête et le message d'erreur est affiché en dessous (carré rouge).

![Interface du système](img/poc-interface-highlight.png){#fig:poc-ui width=85%}

## Tests

Il est possible de tester toutes les attaques en mettant en place un réseau BLE de test. Toutes les attaques ne ciblent jamais plus de 2 appareils BLE. Il est possible de reproduire les conditions attendues dans l'attaque en imitant un esclave et un maître BLE avec des requêtes et réponses préprogrammées. Sur chaque attaque demande des conditions de départ différentes, les appareils peuvent être en attente (émettant des annonces), en appairage ou connectés.  
Une fois notre réseau test mis en place, l'attaque est executée sur celui-ci et les résultats obtenus comparés par rapport à ceux préprogrammés dans le test.

Il est possible d'automatiser ces tests avec 5 appareils (4 dongles et 1 sniffer) branchés à la machine réalisant ceux-ci. Le sniffer réalise la plupart des tàches purement offensive, 2 dongles mettent en place le réseau test pendant que les 2 autres permettent l'usurpation d'identité.

## Livrables

Code source du système fonctionnel: comprend l'intégration de l'outils offensive, le serveur et client pour l'interface ainsi qu'un moyen de déployer le système (Docker).

Documentation du système: rédigée en langage spécifique (markdown, rst) et déployable avec un outils (Sphinx, pandoc), documentation développeur pour mettre en place le système et documenter les choix techniques.

Rapport de projet: rédigé avec un outils spécifique (LaTeX, pandoc), rendue au format PDF, comprend une étude du contexte, analyse de l'existant et de faisabilité puis mise en place de la preuve de concept.

################################################################
################################################################
################################################################
################################################################
################################################################
################################################################
################################################################
################################################################
################################################################
################################################################
################################################################
################################################################

# Preuve de concept

## Scan

Adv ok seulement 3 channels, utilisation du sweeping sur 1 micro bit

Data difficile car 37 channels et transmissions non constantes dans chaque channel, meme avec sweeping sur 1 micro bit ne peut intercepter que 1/37e des communications, jeu chat et souris car appareils hop et bbc sweep pour trouver des comms

## Localisation

TODO differentes methodes de localisation
- avoir une distance (rssi / toa)
- avoir un point dans l'espace (aoa/aod ou trilateration/triangulation)

### RSSI

incertitude rssi +-6dbm et fortement influence par environnement

peu etre reduit avec echantillonage sur le temps, modele de calculs et filtres (kalmann)

BLE utilise plusieurs puissance emissions donc besoin d'une valeur ref pour estimer distance depuis RSSI. Valeur generalement RSSI mesure a 1m par le constructeur et exposee dans les annonce ou en tant que service et nommee txpower (standardisee par GAP/GATT).

TODO formule distance
env factor = 2 pour IPS

### Fingerprinting

A partir d'une liste de beacons et leurs position, calcul la position se rapprochant le plus d'un des beacons (a partir du RSSI).

Demande de pouvoir etablir la liste des beacons et les identifies de facon sure. Si le systeme est mit en place pour cet effet on s'assurera qu'ils soient identifiables (MAC unique par exemple) mais dans notre cas de recuperation d'information, les appareils peuvent mettre en place des mesures contre le tracage comme la generation d'adresse mac aleatoire.
Il est possible d'utiliser le profile GATT pour identifier un appareil, combiner avec le RSSI dans le temps et les deplacements (capteurs) on peut esperer distinguer deux profils GATT identiques.

~ beacons coverage

Le beacon le plus proche

### RSSI / TOA

~ m

Trilateration determines the position of an object
by understanding its distance from three known
reference points. In the case of Bluetooth, locators
estimate their distance to any given asset tag based
on the received signal strength from the tag

### AOA / AOD

~ cm

Basee sur le nouveau systeme d'angle du BLE 5.1
Demande du materiel en plus (Multiple antennes directionnelles pour former une matrice)
Differentes facon de calculee (angle arrivee, angle depart ...)

https://www.bluetooth.com/blog/bluetooth-positioning-systems/
https://www.bluetooth.com/bluetooth-resources/enhancing-bluetooth-location-services-with-direction-finding/?utm_campaign=location-services&utm_source=internal&utm_medium=blog&utm_content=bluetooth-positioning-systems


### Ajouter de la precision

Fusionner les resultats avec un filtre kalmann:
- dead reckoning
- trilateration / triangulation

Ou RSS (range) + AOA (direction)

### RSS

1. Scan devices
   BTLEJack sniffer
2. find settings (rssi, txPower / measured power ...)
   Tx Power service 0x1804 and Tx Power Level Characteristic 0x2A07
3. calculate distance (in a circle around you)
   10 ^ ((txPower – RSSI)/(10 * N))
   N = loss factor (between 2 and 4), 0 for optimal conditions
4. cross multiple references to determine a position (trilateration)
   repeat 3 times to 3 devices
   get OUR position

### AOA

## Spoof

## Hijack

-->