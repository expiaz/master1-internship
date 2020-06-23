```{=latex}
\clearpage
```

# Travail réalisé

## Scan

Le scan des appareils et connexions BLE alentours se base sur un sniffer BLE, la carte BBC micro:bit dans mon cas. Les fonctionnalités de scan sont nativement supportée par Mirage et intégrées dans le firmware adéquat au framework.  
C'est l'une des deux attaques retrouvé dans le front-end: l'utilisateur peut commencer un scan qui notifiera le front-end lors de découvertes, puis l'arrêter quand bon lui semble. Les appareils et connexions répertoriées ainsi que leurs informations sont disponibles sur la colonne de droite (voir @fig:front-lists).

![Appareils et connexions repertoriées à proximité](img/lists.png){#fig:front-lists width=70%}

La carte BBC micro:bit n'intégrant qu'une puce nRF51, une seule commande peut être réalisée à la fois, Mirage met cependant en place du balayage de canaux basé sur un changement rapide de commandes directement dans le firmware via les minuteurs disponibles sur la carte. Ce balayage est notamment utilisé pour la découverte d'appareils BLE sur les canaux d'annonces 37, 38 et 39 ainsi que l'interception de connexions sur les 37 autres canaux de données.  
Le sniffing des connexions est peu fiable dû au changement impredictible de canaux imposé par le *channel hopping*. Cette mitigation intégrée au protocole BLE rend incertain le temps pour identifié une ou plusieurs connexions BLE, la carte micro:bit changeant elle aussi de canaux pour maximiser ces chances de trouver des connexions les utilisants.  

Cette attaque profite du caractère publique des canaux utilisés pour les communications, il est possible de mitiger son impact en rendant plus difficile l'identification des appareils par la réduction du nombre d'annonces émises et en choisissant le type d'annonce en fonction des besoins. Il n'est pas toujours necessaire d'emettre des annonces indirecte contenant des données du *GAP*, les annonces directes contiennent par exemple seulement le *central* recherché, rendant plus complexe la tache d'identification de l'appareil. La découverte des connexion peut egalement etre durcie en modifiant les parametres de connexion émis, plutot que d'utiliser une carte des canaux par defaut se basant sur les 37 canaux de donnees.

## Localisation

Il existe plusieurs moyens de localiser des appareils, la localisation interieur est d'ailleurs un champ de recherche complexe et tres actif allant de l'inventaire d'entrepots jusqu'au profilage publicitaire.  
Pour obtenir une estimation de la distance d'un appareil on peut se basé sur le temps que met l'onde a nous parvenir (appelé *Time Of Arrival* ou *TOA*) pour en deduire la distance a partir de sa vitesse. Cependant cela requiert une information fournie par l'emetteur: l'heure d'émission, en me placant en tant qu'attaquant je ne controle pas les appareils ciblés et ne peut pas garantir la presence de cette information car peu utilisée dans les appareils particuliers.  
Une autre methode beaucoup plus populaire et accessible se base sur le *RSSI* (*Received Signal Strength Indicator*). C'est un indicateur de la puissance du signal reçu en `dBm` duquel peut etre deduit la distance de l'emetteur. Le BLE peut emettre sur une plage de puissances, il est donc necessaire de connaitre ou trouver la puissance d'emission utilisée de la part de l'emetteur. Un standard a ete developpé pour les beacons, nommé iBeacon et intégré dans le *GAP* et le *GATT* en tant que *Tx Power* (puissance de transmission), il fourni une valeur de calibrage représentant la puissance mesurée par le constructeur a 1 metre. Meme si sa presence n'est pas garantie, le standard est tres répandu dans les appareils domestique et de bureautique.  
Les entrepots et centres commerciaux utilisent sur le *fingerprinting*, c'est a dire le positionnement par rapport a des appareils proche identifiés. Chaque appareil est répertorié avec sa position et son calibrage, l'objet a localiser applique ensuite une *trilateration* a partir de la position de 3 appareils a proximité. Cette solution n'est adaptée a mon besoin car elle demande une information indisponible en tant qu'attanquant: la liste des appareils identifiés.

Ensuite viens une seconde problematique, le *TOA* et *RSSI* ne fournissent pas d'information sur la direction de l'appareil, seulement une distance. Il faut alors croiser plusieurs relevés avec de la trilatération, procedé au coeur du systeme GPS visant a trouver une intersection commune entre minimum 3 cercles (voir @fig:methodes-localisation), ou utiliser une matrice d'antennes pour calculer la direction du signal reçu.  
Le BLE intègre depuis la version 5.1 le mecanisme d'angles de départ et d'arrivée (*AOA*/*AOD*) permettant de trouver la direction a l'aide d'une matrice d'antennes. Chaque antenne recois le signal avec un decalage par rapport a ses voisines, ce decalage temporel est utilisé pour approximer l'angle d'emission. En utilisant cette technique, et a partir de plusieurs emetteurs, on peut determiner une position sans se baser sur le *RSSI* ou *TOA* mais en utilisant la *triangulation*.

Pour ma part, je travail sur la version 4.0 du protocole BLE, qui n'integre pas le mecanisme *AOA*/*AOD*. Meme si il est possible de mettre en place cette methode sans la version 5.1 du BLE, cela requiert une matrice d'antennes, materiel indisponible au vu des conditions exceptionnelles.  
J'ai opté pour le *RSSI* au vu de la popularité et facilité de mise en place de la methode. Les relevés sont fortement impactés par l'environnement, l'etude de celui-ci et la mise en place de modeles etant impossible dans mon cas, j'ai fixé le facteur environnmental à 2. Je laisse tout de meme la possibilite a l'utilisateur de modifier ce facteur si besoin. Le second facteur est la sensibilité de reception, la puce nRF51 garantie une valeur à plus ou moins 6dBm avec un seuil de -30 a -90dBm, mon but est donc de reduire l'impact des ecarts de releves.

### Precision

Pour les appareils en mouvement on peut ajouter de la precision avec le *dead-reckoning*, permettant de faire des previsions de position a partir de celle actuelle et des capteurs intégrés a l'appareil (gyroscope, accelerometre). On retrouve ce mecanisme pour les appareils ou applications GPS, tirant avantage des capteurs integres dans nos smartphones. Des modeles mathematiques comme le filtre de Kalman permettent egalement d'approximé les prochaines valeurs.

Le fait de se placer en tant qu'attaquant donc de ne pas controller les appareils rend le *dead-reckoning* inutilisable. 
J'ai choisit le modèle de pertes le plus frequement utilisé pour le *RSSI* car un modele de pertes personnalisé pour un environnement donné n'est pas envisageable puisque le projet est fait pour de la sensibilisation et est donc amené a en changer frequement.  
Dans le but de reduire les ecarts, j'ai commencé par un lissage des valeurs sur une fenetre modifiable. Cela me permet de confirmer une tendance, minimisant l'impact des fluctuations du *RSSI*. Le filtre de Kalman semble etre une amelioration interessante et pourrait etre une prochaine etape.

### Intégration

Dans Mirage, la localisation se base sur le travail d'identification precedement realisé par la phase de scan. Le firmware Mirage integre des informations relevees depuis la puce nRF51 sur la transmission reçu comme la puissance du signal (*Received Signal Strength Indicator* ou *RSSI*). A partir de cette information ainsi qu'un calibrage (`TxPower`) il est possible d'approximer la distance avec le modele de pertes suivant[@rssi-path-loss]:

$$distance = 10^{(TxPower - RSSI) / (10 * n)}$${#eq:distance-equation}

Ou `n` est le facteur environnemental variant de 2 (espace dégagé) à 4 (zone urbaine).

module ble_locate

Une carte permet de se faire une idée de la distance des appareils localisés. La carte à une échelle relative a l'appareil le plus eloigné car le BLE a une portee d'emission d'environ 10 metres, ce qui renderait indistinctibles les appareils proches si la carte couvrait toute la zone d'emission. Les autres appareils sont mis a l'echelle relativement par rapport au plus eloigné pour garder une representation realiste.

![Carte des appareils localisés](img/radar.png){#fig:radar width=50%}

Cette attaque concerne seulement les appareils implemetant le standard iBeacon. D'une facon plus generale l'attaque est facilement mitigable en ne transmettant pas d'indication de distance dans le *GAP*, l'exposant uniquement dans le *GATT* une fois le *central* identifié. Même si les beacons sont forcés d'inclure ses indications dans le *GAP*, ils ne sont pas concernés par la plupart des attaques car non connectables.

BBC MicroBit
Localisation des appareils annoncant alentours avec RSSI et calibrage
Standard iBeacon, fuite d'info GAP
Appareils bureautique (smartphones, pc, ecouteurs etc), beacons pub
Extraction rssi depuis firmware microbit, equation distance avec rssi et txpower lissé sur le temps pour reduire fluctuation
Calibrage necessaire par la cible car BLE difference puissances emissions, seuil sensibilité micro bit base nRF51 +-6dbm, fluctuation rssi
Reduire payload adv GAP, utiliser type ADV correspondant (pas adv_ind tout le temps), certains ne contiennent pas de payload

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

Deux dongles CSR4.0
Clonage et usurpation du *peripheral* dans l'attente d'une connexion du *central* pour voir/modifier puis relayer le traffic.
Appairage sans authentification, methode de chiffrement faible (crackle pour briser le chiffrement car acces connect req)
Objets connectes autonomes
Module mirage ble_mitm
Etre au bon endroit au bon moment, *peripheral* non connecté et *central* intention de connexion, phase appairage presente (non bonding)
Utilisation de methodes d'appairage authentifiee comme PassKey ou NumComp + utilisation connexion securisee LE + mise en place de session LTK

## Hijack

Matos
Fct
Vulns abusees
Cibles
Implementation
Difficultes
Mitigations/protections

Utilise MicroBit et CSR4.0
Prendre place d'un appareil dans une connexion. Se base sur ecoute passive puis brouillage
Pas d'appairage
Capteurs/actionneurs (lampes)
Module mirage ble_hijack
Pas acces a phase de connexion ni d'appairage => demande recover parametres de connexion
Mitigé par channel hopping, protegé par appairage

## Tests et validation

scenarios sur ble-master et slave
A partir de reseau de test mis en place avec Mirage mock master et slave avec 2 CSR4.0
Connexion factice car aucun appareil BLE (coronavirus modification du sujet)

Scan
Connexion longue et incertaine

Locate
demande txpower pour localiser car calibrage BLE
Valeurs +/-30cm, seuil sensibilité -45dBm to -70dBm dans les faits (-30 to -90 sur le papier)

MITM
Manque device pour test

Hijack
Longue et incertaine

## Améliorations

Scan / Hijack connexion
parrallelisation de sniffers pour augmenter les chances de trouver les canaux de donnees utilises

Locate
best multiples antennes AOA/AOD pour augmentation de precision
sinon avoir plus de points de mesures (min 3) avec RSSI
ajouter des methodes d'amelioration precision RSSI (path loss modele, filtre kalmann ...)


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