
# Bluetooth Low energy

Le protocole a ete designé par Nokia et d'autres entreprises pour repondre au besoin d'un protocole sans fil peu gourmand en energie pour les peripheriques personnels (telephone portable, montre, casque). Nommé Wibree, il a ete integre au standard Bluetooth sous le nom *Low Energy*.  
Le Bluetooth ne comprend pas seulement un protocole mais une multitude d'entre eux (BR, EDR, HS) qui ont en commun de permettre la communication (et l'echange de donnees) sans fil avec des peripheriques personnels. Ils font partit des protocoles WPAN (reseau personnel sans fil) et leur distance d'emission est de quelques metres jusqu'a 30 metres.  
La specification Bluetooth 4.0, sortie en 2011, integre le protocole LE (Low Energy) et permet au Bluetooth de touché le marché des systemes embarques, fonctionnants sur batterie.

## Différences

Les autres protocoles du Bluetooth sont principalement connus et utilises pour le transfert de contenu multimédia, que ce soit des fichiers entre ordinateurs comme de la musique avec un casque ou encore une voiture. Ils fonctionnement avec une connexion continue et un transfert en flux.  

Le BLE, visant a reduire la consommation d'energie, n'etablie pas de connexion continue. L'appareil reste la plupart du temps en mode veille, pouvant emettre des annonces, dans l'attente d'une connexion qui aura pour effet d'arreter la transmission d'annonce. Pour chaque requete recu, une reponse pourra etre renvoyee directement ou une notification mise en place periodiquement.

Les appareils BLE et Bluetooth BR/EDR ne sont pas compatibles, n'utilisant pas les memes technologies, protocoles et repondant a des besoin differents (voir @tbl:bluetooth-use-case).

| **Besoin** | Flux données | Transmisson données | Localisation | Reseau capteurs |
| --- | --- | --- | --- | --- |
| **Appareils** | ordinateur, smartphone, casque, enceinte, voiture | accessoires bureautique ou fitness, equipement medical | beacon, IPS, inventaire | automatisation, surveillance, domotique |
| | | | | |
| **Topologie** | point à point | point à point | diffusion (1 à N) | mesh (N à N) |
| | | | | |
| **Technologie** | Bluetooth BR/EDR | Bluetooth LE | Bluetooth LE | Bluetooth LE |

: Cas d'utilisation et protocole Bluetooth adapté {#tbl:bluetooth-use-case}

## Protocole

Pour permettre une interoperabilité maximale entre les appareils BLE, le standard defini 4 profiles en fonction du role de l'appareil: Peripheral, Central, Broadcaster, Observer. Ces roles constituent le *GAP* (*Generic Access Profile*).  
Chaque appareil se conformant au standard ne doit implementer qu'un seul de ces roles a la fois.

Le *Broadcaster* ne communique qu'avec des annonces, on ne peut pas s'y connecter. Ce mode est tres populaire pour les beacons. L'*Observer* est sont opposé, il ne fait qu'ecouter les annonces, n'etabliera jamais de connexion.

Le *Peripheral* et le *Central* forment la seconde pair et permettent la mise en place d'une architecture client-serveur. Le *Peripheral* joue le role du serveur et est dit *esclave* du *Central* qui endosse le rôle du client et *maître*.  
L'esclave transmet des annonces jusqu'a recevoir une connexion d'un maitre, apres quoi il arrete de s'annoncer car il ne peut etre connecté qu'a un maitre a la fois. Le maitre ecoute les annonces d'esclave (annonces connectables) pour se connecter, puis interroge ses services via le *GATT* (*Generic Attribute*).

### Couche physique

Le BLE opère dans la bande ISM 2.4GHz tout comme le Wi-Fi. Contrairement aux canaux Wi-Fi de 20MHz, le BLE découpe le spectre en 40 canaux de de 2MHz (plage de 2400 à 2480MHz).  
Le protocole met en place le *saut de fréquence*, consistant à changer de canal d'émission tout les laps de temps donné, pour réduire le risque de bruit sur les fréquences utilisées (la bande ISM 2.4Ghz étant libre d'utilisation).  
Sur les 40 canaux que compose le spectre, 3 sont utilisés pour la transmission d'annonce. Ils sont choisit pour ne pas interferer avec les canaux Wi-Fi car les deux protocoles sont amenés à coexister (voir @fig:ble-channels).  
Les 37 autres canaux sont utilisés pour les connexions. Chaque connexion va utiliser un sous-ensemble des 37 canaux (appelé carte des canaux) pour éviter les interferences avec les autres connexions BLE. Un seul canal transmet des donnees a la fois mais tous les canaux de la carte sont utilises pour le saut de frequences.

![Répartition du spectre BLE en canaux^[https://www.accton.com/Technology-Brief/ble-beacons-and-location-based-services/]](img/ble-chan.jpg){#fig:ble-channels width=90%}

### Couche logique

![Étapes d'un échange BLE](img/ble-conn.png){#fig:ble-conn width=70%}

#### 1. Annonces

L'esclave indique sa présence avec des annonces émises périodiquement. Ces annonces contiennent sont addresse Bluetooth (permettant une connexion) et des données qui consituent un profile (appelé *GAP*[^gap]). Ces données permettent aux maîtres de savoir si il est capable de realiser les fonctionnalités recherchées.  
La specification Bluetooth definit des profiles type pour des applications communes dans les appareils BLE[^gatt]. Cela inclus par exemple les capteurs corporels pour le sport, les capteurs médicaux de surveillance (pour les diabetiques notamment), la domotique (termometres, lampes), etc.

Dans un environnement BLE, les maîtres ne peuvent pas reconnaitre leurs esclaves a part avec une addresse Bluetooth fixe, mecanisme de moins ne moins utilisé car vulnérable a l'usurpation. Les esclave generent donc des addresses aleatoires et l'identification se fait via les donnees du *GAP* contenues dans l'annonce. Ce mecanisme permet a n'importe quel maitre de s'appairer a n'importe quel esclave proposant le profil recherché.  
Par exemple, une application de smartphone BLE pouvant gerer la temperature pourrait s'appairer et utiliser n'importe quel appareil BLE qui implemente le profil standardisé pour les termometres dans le *GAP*.  
Les profils ne sont certes pas exhaustifs mais permettent une integration fonctionnelle avec un maximum d'appreils et prévoient un moyen d'integrer des donnees proprietaires non standardisées[^gap-ext].

[^gap]: https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile/
[^gatt]: https://www.bluetooth.com/specifications/gatt/services/
[^gap-ext]: https://www.silabs.com/community/wireless/bluetooth/knowledge-base.entry.html/2017/02/10/bluetooth_advertisin-hGsf

#### 2. Connexion

Lorsqu'un maitre recois une annonce d'un esclave auquel il souhaite se connecter, il lui envoit une intention de connexion sur les canaux d'annonce. Ce message contient tout les parametres communs pour etablir une connexion sur les canaux de donnees: carte des canaux utilisés, temps entre chaque saut de frequence, nombre de canaux sautés par saut, addresse unique de la connexion (appelée *Access Adress*).

Ce message (nommé *CONNECT_REQ*) est crucial lors d'attaques car il permet la synchronisation avec une connexion pour l'ecoute passive et est donc jugé sensible puisque transmit sur les canaux d'annonces avant la mise en place du chiffrement.

#### 3. Capacités

Le BLE voulant garder une interoperabilité maximale entre les appareils et tout les appareils ne disposant pas des memes fonctionnalites embarques, il est definit plusieurs methodes d'appairage en fonction des capacites disponibles sur les deux appareils.

Chaque appareil va transmet ses capacités a l'autre ainsi que ses exigences sur la connexion a etablir. Les capacités sont deduites des fonctionnalités presentent physiquement sur l'appareil et les exigences de la version du procole actuellement supportée par celui-ci.  
Les exigences comprennent la protection aux attaques *MITM* par l'authentification de l'appairage, l'etablissement d'une connexion sécurisée (*LE secure connection*), la mise en place d'une session (*Bonding*) pour une reconnexion future ainsi que l'utilisation d'un canal autre que le BLE (comme le *NFC*) pour la transmission de secrets menant au chiffrement (*Out Of Band*).

| Capacité | Description |
| --- | --- |
| No input | pas la capacité d'indiquer *oui* ou *non* |
| Yes/No | mécanisme permettant d'indiquer *oui* ou *non* |
| Keyboard | claver numérique avec mécanisme *oui*/*non* |

: Capacités d'entrée possibles^[https://www.bluetooth.com/blog/bluetooth-pairing-part-1-pairing-feature-exchange/] {#tbl:ble-input-caps}

| Capacité | Description |
| --- | --- |
| No output | pas la capacité de communiquer ou afficher un nombre |
| Numeric Output | peut communiquer ou afficher un nombre |

: Capacités de sortie possible {#tbl:ble-output-caps}

| | No output | Numeric output |
| --- | --- | --- |
| No input | NoInputNoOutput | DisplayOnly |
| Yes/No | NoInputNoOutput | DisplayYesNo |
| Keyboard | KeyboardOnly | KeyboardDisplay |

: Capacité d'entrées/sorties de l'appareil {#tbl:ble-io-caps}

#### 4. Appairage

En fonction des capacites et des exigences emits par chacun des appareils, une methode d'appairage est selectionnée (voir @tbl:ble-pairing-methods).

| | **DisplayOnly** | **DisplayYesNo** | **KbdOnly** | **NoIO** | **KbdDisplay** |
| --- | --- | --- | --- | --- | --- |
| **DisplayOnly** | JW | JW | PK | JW | PK |
| **DisplayYesNo** | JW | JW/NC | PK | JW | PK/NC |
| **KbdOnly** | PK | PK | PK | JW | PK |
| **NoIO** | JW | JW | JW | JW | JW |
| **KbdDisplay** | PK | PK/NC | PK | JW | PK/NC |

: Méthode d'appairage utilisée en fonction des capacités échangées^[https://www.bluetooth.com/blog/bluetooth-pairing-part-2-key-generation-methods/] (JW=JustWorks PK=PassKey NC=NumComp) {#tbl:ble-pairing-methods}

Je m'interesse principalement a la methode *JustWorks*. C'est la methode par defaut lorsque deux appareils ne disposent pas des capacites necessaires pour une autre. Elle est notamment utilisee dans les objets connectes puisqu'ils n'integrent pas de mecanisme pour un appairage plus complexe.  
*Passkey* et *NumComp* permettent d'authentifier l'appairage pour se proteger des usurpations d'identite (*MITM*) puisque partageant un secret via l'utilisateur (ou un autre canal dans le cas du *OOB*). *JustWorks* ne permet pas d'authentifier les appareils et le chiffrement est moins robuste que les autres methodes mais permet tout de meme d'etablir une communication chiffree.  

La méthode d'appairage choisie permet de transmettre un des materiaux cryptographique: la clef temporaire (ou *Temporary Key*). Cette phase est plus ou moins sensible à l'ecoute passive en fonction de la methode d'appairage et des exigences emits lors de l'echange des capacites.  
*JustWorks* avec connexion BLE 4.0 (dite *legacy*) est le mode le plus sensible puisque la clef temporaire est tout simplement zéro, ne disposant pas de moyen de transmettre une données par autre voie, et peut donc etre trouvee rapidement par bruteforce.

La connexion *LE secure*, introduite a partir de la version 4.2, utilise l'algorithme Diffie-Hellman (*ECCDH* exactement) pour l'echange des materiaux cryptographiques et est donc resistante a l'ecoute passive (*eavesdropping*) mais toujours vulnerables a l'usurptation d'identite (*MITM*) avec certaines methodes d'appairage (*JustWorks*).

#### 5. Echange de clefs

L'etablissement du chiffrement de la connexion est ensuite realisé par derivation a partir d'une premiere clef temporaire transmise via la methode d'appairage choisie et d'autre parametres echanges via le protocole BLE.
La clef obtenue est dite court terme (*Short Term Key*) car elle ne sera utilisee que pour cette connexion et devra etre re-generee a chaque nouvelle connexion.

Dans le cas des connexion securisees, l'algorithme *ECCDH* est utilisé pour échanger la clef temporaire duquelle une clef long terme (*Long Term Key*) est dérivée.  
Il est possible de reutiliser les clefs long terme avec la mise en place d'une session si cela a ete exigé lors de l'echange des capacités. La clef long terme (*LTK* pour *Long Term Key*) est stockée et associée à l'appareil communiquant pour rétablir une connexion future sans avoir à refaire une phase d'appairage.

A partir de la comprehension actuelle du protocole BLE et du fonctionnement de l'appairage, il semble recommandé de mettre en place une connexion securisee des que possible. Il est egalement necessaire d'eviter la methode *JustWorks* au maximum.  
Cependant, il est assez simple de forger un echange de capacités pour retrograder la connexion en *legacy* et forcer *JustWorks* via les capacités echangees.  
C'est pourquoi certains appareils attendent des capacites et exigences minimales pour etablir une connexion, sans quoi celle-ci est avortee. C'est notamment le cas d'appareils proprietaires concus pour fonctionner ensemble.

#### 6. Requêtes

Les échanges sont realises sur la base d'une architecture client-serveur. Le maître (client) interroge l'esclave (serveur) avec le protocole *ATT* (*ATTribute Protocole*).  
Chaque requete mene soit a une reponse du serveur soit a la mise en place d'une notification lors d'un evenemment (valeur changée ou disponible).

Les requetes et reponses possibles sont standardisées sous le *GATT* (*Generic ATTributes*) pour permettre une interoperabilité maximale entre les appareils (comme pour le *GAP*). *GATT* et *GAP* partagent les memes profiles, seul la structure change. Le serveur *GATT* peut etre interrogé pour etablir une liste exhaustive de toutes les fonctionnalites d'un appareil la ou le *GAP* choisit ce que contient l'annonce mais est limite par la taille du paquet (31 octets).

### GAP

Dans le cas des *Peripherals* et *Centrals*, le *GAP* est principalement utilisé pour etablir un profil de l'esclave permettant la decision de connexion de la part du maitre.  
Pour les *Boardcasters* et *Observers* il permet la communication unidirectionnelle (*Broadcaster* vers *Observer*) via les annonces, ceux-ci utilisant la diffusion plutot qu'une connexion point a point. On retrouve cette utilisation pour les beacons publicitaires ou de localisation interieur.

### GATT

Pour l'echange de données lors de connexion point à point, le *GATT* est utilisé en mode client-serveur. L'architecture du serveur *GATT* est en entonnoir, la plus haute couche s'appelle un *service*, il encapsule des *caracteristiques*, chacune contenant un *attribut* (valeur) et un ou plusieurs *descripteurs* fournissants des informations additionnelles sur l'attribut (voir @fig:ble-gatt-arch).  
A chacune de ses couches (service, caracteristique, attribut, descripteur) est attribué un identifiant unique appelé *handle*. La plage des indentifiant est partagée entre toutes les couches donc si un service a l'identifiant `0x01` aucun autre service/caracteristique/attribut/descripteur ne peut l'utiliser.

Un service correspond generalement a un profil (standardise ou non) comme un termometre par exemple. Ce service exposerait des caracteristiques comme la temperature, l'humidite ou autres. Chacune de ces caracateristique contient la valeur (donnée brute) et les descripteurs peuvent indiquer l'unité ou encore un facteur ou formule pour convertir la valeur donnée en resultat exploitable.

A moins de connaitre exactement l'appareil et de l'interroger en mode aveugle via les identifiants (ce qui peut etre le cas entre des appareils proprietaires), il faut proceder par etape en decouvrant d'abors les services disponibles, puis chaque caracteristique par service et enfin les attributs de celles-ci.  
Pour proceder a cette decouverte d'un appareil, le protocole *ATT* dispose d'un type de requete par couche a interroger (voir @fig:ble-gatt-arch). Une fois le service voulu trouvé (ou la cartographie totale de l'appareil realisée), on peut lire, ecrire ou souscrire a des attributs directement par *handle*. Le *GATT* met en place un systeme de droits par attribut pour proteger la lecteur, l'ecriture et la souscription par le client.

Le *GATT* définit egalemet des services standardisés appelé primaire et secondaire censés etres present sur tout les appareils BLE afin de connaitre les fonctionnalites principales de l'appareil. Comme les *handle* sont definies arbitrairement par le serveur *GATT*, ces services sont identifiés par un *UUID* identique dans tout les appareils BLE [^gatt-std-services].

[^gatt-std-services]: https://www.bluetooth.com/specifications/gatt/services/

![Client et serveur GATT^[https://fr.mathworks.com/help/comm/examples/modeling-of-ble-devices-with-heart-rate-profile.html]](img/ble-gatt-arch.png){#fig:ble-gatt-arch width=70%}

## Versions

Depuis sa premiere iteration en 2011 dans la version `4.0` des specifications Bluetooth le BLE a evoluer pour integrer des mesures de securite avec l'ajout des connexions securisees LE en `4.2` puis la diversification des topologies avec l'introduction du *mesh* pour les reseaux de capteurs en `5.0` et dernierement l'amelioration de la localisation interieur (*Indoor Positionning System*) pour une precision de l'ordre du centimetre grace aux systemes angle d'arrivée et de depart (*AOA/AOD*).