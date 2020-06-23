```{=latex}
\clearpage
```

# Étude de l'existant

## Outils

Les outils offensifs sur le protocole BLE permettent de recuperer, analyser et modifier les echanges entre appareils permettant de realiser des audits de securite ou mettre en place des attaques exposant des vulnerabilites. L'analyse du traffic sans fil BLE demande une antenne couvrant la bande utilisee par les 40 canaux du protocole ainsi qu'un systeme assez rapide pour scanner puis suivre les communications lors des sauts de frequence. Les radio-logiciels (*SDR*) ne sont donc pour la plupart pas adaptés car trop lents ou trop cher pour les fonctionnalités voulues: des outils specialises dans l'analyse et l'attaque du BLE sont disponibles pour une fraction du prix.

Le premier outil, utilisé dans tout nos appareils BLE, est la puce intégrée pour les communications BLE. La recuperation (*sniffing*) et analyse ou modification d'un traffic sans fil etant interdit, ces puces utilisent un *firmware* proprietaire conforme aux roles determinés dans les specifications BLE. Même si il reste possible d'analyser le traffic (notamment en utilisant *Wireshark*[@wireshark]) entre la puce et un appareil BLE, il n'est pas possible d'etendre les capacites de celle-ci sans modifier le *firmware*.  
Tout les appareils ne disposant pas d'une puce BLE dédiée, les constructeurs ont developpes des *dongles* integrant ces puces et permettant de communiquer avec tout appareil USB via une interface nommée *HCI* (*Host-Controller Interface*). Allié aux outils standard du protocole BLE comme *BlueZ*, la pile protocolaire BLE du noyau Linux, ces *dongles* permettent de découvrir les appareils a proximité et d'endosser le role de *peripheral* ou *central* pour etablir une communication avec n'importe quel autre appareil BLE. Les utilitaires *hcitool*, *hciconfig* et *gatttool* de *BlueZ* permettent par exemple de manipuler les annonces et extraire le profil *GATT* d'un appareil BLE. Meme si certains de ces *dongles* proposent des fonctionnalites interessantes comme le changement d'adresse Bluetooth (*Bluetooth Address* ou *BD*), ils n’ont pas été conçus dans une optique de sécurité, et sont peu flexibles pour un usage offensif.

La plupart des attaques sur le protocole BLE requierts un moyen d'intercepter le traffic. Les *dongles* et *puces* embarquants des firmware ne permettant pas cette fonctionnalite puisque destines au grand public, beacoups d'outils specialises ont etes developpes. On va retrouver des outils d'analyse de protocole sans fil generaux comme la *HackRF* ou sa version specialement concue pour le BLE nommée *Ubertooth One*. Ces cartes sont assez cher mais hautement personnalisables depuis les couches bas niveau. Elles demandent un certain background de connaissances sur le protocole et les modulations sans fil pour arriver a un resultat precis (comme la realisation d'une attaque).  
Viennent ensuite les *sniffers* sous forme de dongle USB arrangées et plus ou moins personnalisables. Beaucoup sont basés sur les memes puces de *Nordic Semiconductor* ou *Texas Instrument* qui eux meme proposent leurs sniffers[@nrf-dongle;@ti-dongle] et logiciels[@nrf-soft;@ti-soft] pour l'analyse du protocole BLE. Dans les initiatives plus open-source, mais pas encore totalement personnalisable sans reprogrammation de la puce, on peut citer le Bluefruit[@bluefruit] de *Adafruit*.  
Enfin, un outils open-source nommé *BTLEJack* permet non seulement l'etude mais la mise en place d'une multitude d'attaques sur le protocole Ble via reprogrammation de la carte avec un firmware personnalisé. Cet outils a ete developpe pour la carte *BBC Micro:Bit*[@microbit], une carte de developpement bon marché a but educatif, et est aujourd'hui compatible avec plusieurs autres cartes intégrant une puce `nRF51` (notamment la *Bluefruit*).
Basé sur les travaux de *BTLEJack*[@btlejack] et d'autres librairies BLE en python, *Mirage*[@mirage] permet des fonctionnalités identiques en supportant encore plus de cartes, de protocoles et d'attaques. Il comble le manque de flexibilité des precedants outils en integrant plusieurs mecanismes permettant la mise en place d'attaques scénarisées entierement personnalisees depuis les couches protocolaires basses et facilite l'ajout de fonctionnalités au sein du framework.

## Attaques

### Scanning
Le *scanning* consiste à répertorier des appareils BLE à proximité. Dans le cas d'attaque on etendra l'inventaire avec les connexion établies entre 2 appareils BLE. Là ou les *dongles HCI* suffisent pour intercepter les annonces diffusées, l'analyse des communications établies requiert un *sniffer* capable de suivre les 37 canaux de données.  
La pile protocolaire *BlueZ* permet le *scan* des *advertisements* (annonces) tandis que plusieurs outils precedements evoques comme *smartRF* ou *nRFSniffer* suffisent pour repérer une communication.

### Spoofing
C'est l'une des étape du *Man-In-The-Middle* qui permet d'usurper un esclave BLE. Après identification de la victime (via annonce ou adresse BD), l'attaquant la clone en s'y connectant et extractant son profile *GATT*. L'attaquant peut resté connecté pour garder la victime silencieuse (un esclave connecté n'emettant pas d'annonces) puis, via un second *dongle* BLE, s'annonce comme étant l'appareil precedemment cloné.  
Cette attaque est realisable en utilisant simplement un *dongle HCI* et l'utilitaire *BLueZ*. Les librairies et frameworks d'attaque discutés plus auparavant (*GATTAcker*, *BTLEJack*) integrent egalement ces mecanisme.

### Sniffing
Le *sniffing* est l'analyse voir le suivis d'une connexion BLE (suivant les capacites du *sniffer* utilisé). Un premier cas de figure est l'attente d'une nouvelle connexion pour se synchroniser avec afin de suivre les echanges. La seconde option, et la plus courante, est la synchronisation avec une connexion deja etablie: la difficulté ici réside en la recuperation des parametres de connexion. Il est necessaire de retrouver la carte des canaux utilisés (*channel map*) ainsi que le *hop increment* (nombre de canaux sautés) et *hop interval* (temps entre chaque saut) pour se synchroniser, sans quoi il est impossible de suivre une connexion car les sauts impredictibles et trop frequents.  
*BTLEJack*, et par conséquent *Mirage*, mettent en place un mecanisme permettant de retrouver ces informations de connexion a partir des echanges interceptés lors du *scanning*. Le *sniffing* de communications sans synchronisation quant a lui est une fonctionnalité très répandue et integrée a tout les sniffers BLE vu antierieurement.

### Man-In-The-Middle
L'attaque *Man-In-The-Middle* concerne n'importe quelle communication: l'attaquant peut modifier les communications en vennant se placer entre l'emetteur et le recepteur ciblé, se faisant passer pour l'un apres de l'autre en usurpant leurs identités. Dans le cas du BLE on utilisera deux *dongles*, un pour usurpé l'esclave cible et un autre pour maintenir une connexion avec celui-ci. On doit d'abors usurpé l'esclave cible via du *spoofing* puis attendre la connexion d'un maitre, une fois le maitre connecté à notre *dongle* usurpateur on se retrouve en situation de *Man-In-The-Middle* entre l'esclave et le maitre: on peut suivre et modifier le traffic avant de le retransmettre. A noté que l'on peut egalement usurpé le maitre si les appareils ciblés attendent un appareil précis pour s'appairer.  
Plusieurs outils sont dediés a cette attaque car populaire et simple a mettre en oeuvre: *GATTAcker* et *BTLEJuice* facilitent la mise en place en automatisant les etapes a partir de la cible choisie. Ce sont d'assez ancien outils qui aujourd'hui souffrent de lacunes de part les technologies utilisees. Basés sur *Noble* et *Bleno*, des librairies en JavaScript basées sur NodeJS et permettant de manipuler le BLE, ils manque de flexibilité et ne permettent pas entre autre la coexistence d'appareils BLE, obligant l'utilisation de machine virtuelle pour chaque *dongle*. *Mirage* reprend le fonctionnement de ces outils, l'integrant en tant que module, mais basé sur de nouvelles librairies, notamment *PyBT*[@pybt] permettant de simuler le comportement d'un appareil BLE en s'affranchissant des contraintes imposees par leurs equivalent JavaScript, *Noble* et *Bleno*.

### Jamming
Le brouillage de communication est egalement une attaque assez populaire et implementee dans bon nombre d'outils sur le marché. Le but est de creer du bruit sur le canal au moment de la transmission pour corrompre le message, le rendant inutilisable par le recepteur. Concernant le BLE, *Ubertooth One* dispose des capacités nécessaire pour brouiller les canaux d'annonce ainsi qu'une communication etablie par retransmission simultanee. *BTLEJack* implemente egalement le brouillage au sein de son firmware personnalisé et, ayant deja un mecanisme permettant de se synchroniser avec une communication, peut egalement brouiller une communication etablie.

### Hijacking
Le principe est de voler une connexion entre 2 appareils en forcant une deconnexion de l'un pour prendre sa place. Cette nouvelle attaque, implementée par *BTLEJack* et reprise dans *Mirage*, utilise les différences de *timeout* entre le *central* et le *peripheral* pour forcer le *central*, via l’utilisation de brouillage sur les paquets du *peripheral*, à se déconnecter et prendre ainsi sa place au sein de la communication.

## Mirage

Après comparaison entre les outils disponibles (voir @tbl:ble-tools), j'ai choisie *Mirage* car il dispose de la flexibilite voulue pour implementee des attaques scenarisee: acces aux couches bas niveau pour recuperer informations comme force du signal et calibrage (necessaires pour calculer la position d'un appareil lors de la localisation). Il dispose egalement d'une implementation d'un *central* et *peripheral* personnalisables pour realiser un reseau de tests sur lequel verifie l'implementation des attaques. Enfin, il supporte une varieté de composants matériel[@mirage-devices] ainsi que toutes les attaques necessaires[@mirage-attacks] pour la preuve de concept, rendant le developpement plus simple.

----------------------------------------------------------------------------------------------------------------------------------------------
Logiciel                *scan* *sniff* *mitm* *jam* *hijack* *locate*    Matériel
----------------------- ------ ------- ------ ----- -------- ----------- ---------------------------------------------------------------------
nRFSniffer              oui    oui     non    oui   non      non         puce `nRF51`

TIsmartRF               oui    oui     non    non   non      non         puce `CC25xx`

BTLEJuice               oui    non     oui    non   non      non         *dongle HCI* + *Bleno*/*Noble*

GATTAcker               oui    non     oui    non   non      non         *dongle HCI* + *Bleno*/*Noble*

BTLEJack                oui    oui     oui    oui   oui      non         *BBC Micro:Bit*, cartes basées sur puce `nRF51`

Mirage                  oui    oui     oui    oui   oui      possible    *dongle HCI*, *Ubertooth*, *nRF*, cartes compatibles avec *BTLEJack*
----------------------------------------------------------------------------------------------------------------------------------------------

: Comparaison des outils pour l'étude offensive du BLE {#tbl:ble-tools}

Concernant le matériel necessaire, la preuve de concept necessite d'abors deux *dongles HCI* compatibles avec Mirage et supportant le changement d'adresse *BD* pour le *spoofing*. *Mirage* se base sur les numeros de constructeurs des *dongles* definit par le Bluetooth[@ble-company-id] pour savoir s'ils sont compatibles. Il supporte une variete des constructeur dont le *CSR8510*[@csr8510] de Qualcomm, puce tres populaire dans les *dongles HCI* basiques et permettant le changement d'adresse *BD*.  
Concernant le *sniffer* necessaire pour la pupart des attaques, *Mirage* se basant sur *BTLEJack*, les cartes supportées par celui-ci le sont aussi par *Mirage*. Même si *Mirage* supporte d'autres cartes comme celles de developpement de *Nordic Semiconductor* ou l'*Ubertooth One*, elles ne sont pas adaptées pour mon projet car trop onereuses pour les fonctionnalités exploitees dans la preuve de concept.  
Je me suis donc tourné vers les cartes compatibles avec *BTLEJack*[@mirage-btlejack]. *Bluefruit* d'Adafruit, Waveshare *BLE400*[@ble400] et les kits *nRF51*[@nRF51] demandent une reprogrammation via un peripherique externe utilisant le port *SWD*. Ne disposant pas du materiel necessaire pour la reprogrammation, et celui-ci etant assez onéreux, j'ai choisit la *BCC Micro:Bit*: carte avec laquelle *BTLEJack* à ete originalement developpé.

![carte BBC micro:bit](img/microbit.jpg){#fig:microbit width=30%} ![dongle HCI BLE CSR8510](img/hci.jpg){#fig:hci width=30%}

### Intégration

Mirage est un "*framework offensif pour l'audit des protocoles sans fil*"[@mirage]. Il a ete pense pour le *pentest* (audit de sécurité) donc un usage exclusivement en ligne de commandes (*CLI*). Meme si le framework se veut beaucoup plus modulaire et extensible que ces predecesseurs (BTLEJack notamment), cette modularite a ete pensee pour l'interface en ligne de commandes.  
Mirage fournit des briques logicielles pour communiquer avec des appareils (dongles, sniffers) ainsi que decortiquer les protocoles, ce qui constitue le coeur du framework. Ces briques logicielles de base sont utilisees par des *modules* dans un but precis, par exemple realiser le brouillage d'une communication BLE. Mirage fournie un certain nombre de modules fournissant les attaques retrouvees dans les autres outils d'audit du BLE (*BTLEJack*, *GATTAcker*, ...) precedement discutes. Similaire a la philosophie d'Unix, ces modules sont specialisés dans une tache precise et peuvent etres assemblés entre eux pour realise des fonctionnalites plus complexes comme la connexion avec le module *ble_connect* puis l'extraction d'informations avec *ble_discover*. Enfin, il est possible de modifier les etapes d'une attaque via les *scénarios*: chaque module accepte un scénario surchargeant son flux d'execution et ses methodes.

mirage extensible certes mais seulement en CLI selon ces regles
Pas pense pour vivre dans un back-end, fait pour le pentest: une attaque puis shutdown => etat instable apres une attaque, non fiabilite des appareils utilises pour conduire l'attaque car fermeture des connexions non effectué normalement fait par shutdown de mirage
Creation API pour integration avec Flask mais couches CLI et Modules fortements liées, problemes de personnalisations de l'API sans modifier le coeur des modules ou de mirage => instanciation manuelle de l'app et des modules au besoin

### Interfaces

Inutile et long de reconduire l'interface CLI de mirage en API pour le back, la rendre accessible depuis GUI via websockets puis la rendre en HTML/CSS/JS. Les attaques selectionnees demandent actions utilisateurs car modification a la volee d'informations, seul le scan et localisation sont autonomes. Decision de laisse le front pour demo localisation et scan pour sensibilisation fuite d'informations passive BLE (smartphones, airpods, pc).  
Utilisation CLI Mirage avec modules personnalisés pour conduire les attaques choisies (et meme plus puisque mirage dispose d'une multitudes d'attaques).
