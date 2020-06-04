
# Étude de l'existant

## Outils

Les outils offensifs sur le protocole BLE permettent de recuperer, analyser et modifier les echanges entre appareils permettant de realiser des audits de securite ou mettre en place des attaques exposant des vulnerabilites. L'analyse du traffic sans fil BLE demande une antenne couvrant la bande utilisee par les 40 canaux du protocole ainsi qu'un systeme assez rapide pour scanner puis suivre les communications lors des sauts de frequence. Les radio-logiciels (*SDR*) ne sont donc pour la plupart pas adaptés car trop lents ou trop cher pour les fonctionnalités voulues: des outils specialises dans l'analyse et l'attaque du BLE sont disponibles pour une fraction du prix.

Le premier outil, utilisé dans tout nos appareils BLE, est la puce intégrée pour les communications BLE. La recuperation (*sniffing*) et analyse ou modification d'un traffic sans fil etant interdit, ces puces utilisent un *firmware* proprietaire ne permettant que la communication en *master* ou *slave* et respectant les specifications BLE. Même si il reste possible d'analyser le traffic (notamment en utilisant *Wireshark*^[https://www.wireshark.org/]) entre la puce et un appareil BLE, il n'est pas possible d'etendre les capacites de celle-ci sans modifier le *firmware*.  
Tout les appareils ne disposant pas d'une puce BLE dédiée, les constructeurs ont developpes des *dongles* integrant ces puces et permettant de communiquer avec tout appareil USB via une interface nommée *HCI* (*Host-Controller Interface*). Allié aux outils standard du protocole BLE comme *BlueZ*, la pile protocolaire BLE du noyau Linux, ces *dongles* permettent de découvrir les appareils a proximité et d'endosser le role d'esclave ou maitre pour etablir une communication avec n'importe quel autre appareil BLE. Les utilitaires *hcitool*, *hciconfig* et *gatttool* de *BlueZ* permettent par exemple de manipuler les annonces et extraire le profil *GATT* d'un appareil BLE. Meme si certains de ces *dongles* proposent des fonctionnalites interessantes comme le changement d'adresse Bluetooth, ils n’ont pas été conçus dans une optique de sécurité, et sont peu flexibles pour un usage offensif.

La plupart des attaques sur le protocole BLE requierts un moyen d'intercepter le traffic. Les *dongles* et *puces* embarquants des firmware ne permettant pas cette fonctionnalite puisque destines au grand public, beacoups d'outils specialises ont etes developpes. On va retrouver des outils d'analyse de protocole sans fil generaux comme la *HackRF* ou sa version specialement concue pour le BLE nommée *Ubertooth One*. Ces cartes sont assez cher mais hautement personnalisables depuis les couches bas niveau. Elles demandent un certain background de connaissances sur le protocole et les modulations sans fil pour arriver a un resultat precis (comme la realisation d'une attaque).  
Viennent ensuite les *sniffers* sous forme de dongle USB arrangées et plus ou moins personnalisables. Beaucoup sont basés sur les memes puces de *Nordic Semiconductor* ou *Texas Instrument* qui eux meme proposent leurs sniffers[^nrf-dongle][^ti-dongle] et logiciels[^nrf-soft][^ti-soft] pour l'analyse du protocole BLE. Dans les initiatives plus open-source, mais pas encore totalement personnalisable sans reprogrammation de la puce, on peut citer le Bluefruit^[https://www.adafruit.com/product/2269] de *Adafruit*.  
Enfin, un outils open-source nommé *BTLEJack* permet non seulement l'etude mais la mise en place d'une multitude d'attaques sur le protocole Ble via reprogrammation de la carte avec un firmware personnalisé. Cet outils a ete developpe pour la carte *BBC Micro:Bit*^[https://microbit.org/], une carte de developpement bon marché a but educatif, et est aujourd'hui compatible avec plusieurs autres cartes intégrant une puce `nRF51` (notamment la *Bluefruit*).
Basé sur les travaux de *BTLEJack*^[https://github.com/virtualabs/btlejack] et d'autres librairies BLE en python, *Mirage*^[https://homepages.laas.fr/rcayre/mirage-documentation/index.html] permet des fonctionnalités identiques en supportant encore plus de cartes, de protocoles et d'attaques. Il comble le manque de flexibilité des precedants outils en integrant plusieurs mecanismes permettant la mise en place d'attaques scénarisées entierement personnalisees depuis les couches protocolaires basses et facilite l'ajout de fonctionnalités au sein du framework.

[^nrf-dongle]: https://www.nordicsemi.com/Software-and-tools/Development-Kits/nRF51-Dongle
[^ti-dongle]: http://www.ti.com/tool/CC2540EMK-USB
[^nrf-soft]: https://www.nordicsemi.com/Software-and-tools/Development-Tools/nRF-Sniffer-for-Bluetooth-LE
[^ti-soft]: http://www.ti.com/tool/PACKET-SNIFFER

## Attaques

### Scanning
Le *scanning* consiste à répertorier des appareils BLE à proximité. Dans le cas d'attaque on etendra l'inventaire avec les connexion établies entre 2 appareils BLE. Là ou les *dongles HCI* suffisent pour intercepter les annonces diffusées, l'analyse des communications établies requiert un *sniffer* capable de suivre les 37 canaux de données.  
La pile protocolaire *BlueZ* permet le *scan* des *advertisements* (annonces) tandis que plusieurs outils precedements evoques comme *smartRF* ou *nRFSniffer* suffisent pour repérer une communication.

### Spoofing
C'est l'une des étape du *Man-In-The-Middle* qui permet d'usurper un esclave BLE. Après identification de la victime (via annonce ou adresse BD), l'attaquant la clone en s'y connectant et extractant son profile *GATT*. L'attaquant peut resté connecté pour garder la victime silencieuse (un esclave connecté n'emettant pas d'annonces) puis, via un second *dongle* BLE, s'annonce comme étant l'appareil precedemment cloné.  
Cette attaque est realisable en utilisant simplement un *dongle HCI* et l'utilitaire *BLueZ*. Bien sur, les librairies et frameworks d'attaque discutés plus auparavant (*GATTAcker*, *BTLEJack*) integrent egalement ces mecanisme.

### Sniffing
Le *sniffing* est l'analyse voir le suivis d'une connexion BLE (suivant les capacites du *sniffer* utilisé). Un premier cas de figure est l'attente d'une nouvelle connexion pour se synchroniser avec afin de suivre les echanges. La seconde option, et la plus courante, est la synchronisation avec une connexion deja etablie: la difficulté ici réside en la recuperation des parametres de connexion. Il est necessaire de retrouver la carte des canaux utilisés (*channel map*) ainsi que le *hop increment* (nombre de canaux sautés) et *hop interval* (temps entre chaque saut) pour se synchroniser, sans quoi il est impossible de suivre une connexion car les sauts impredictibles et trop frequents.  
*BTLEJack*, et par conséquent *Mirage*, mettent en place un mecanisme permettant de retrouver ces informations de connexion a partir des echanges interceptés lors du *scanning*. Le *sniffing* de communications sans synchronisation quant a lui est une fonctionnalité très répandue et integrée a tout les sniffers BLE vu antierieurement.

### Man-In-The-Middle
L'attaque *Man-In-The-Middle* concerne n'importe quelle communication: l'attaquant peut modifier les communications en vennant se placer entre l'emetteur et le recepteur ciblés, se faisant passer pour l'un apres de l'autre en usurpant leurs identités. Dans le cas du BLE on utilisera deux *dongles*, un pour usurpé l'esclave cible et un autre pour maintenir une connexion avec celui-ci. On doit d'abors usurpé l'esclave cible via du *spoofing* puis attendre la connexion d'un maitre, une fois le maitre connecté à notre *dongle* usurpateur on se retrouve en situation de *Man-In-The-Middle* entre l'esclave et le maitre: on peut suivre et modifier le traffic avant de le retransmettre. A noté que l'on peut egalement usurpé le maitre si les appareils ciblés attendent un appareil précis pour s'appairer.  
Plusieurs outils sont dediés a cette attaque car populaire et simple a mettre en oeuvre: *GATTAcker* et *BTLEJuice* facilitent la mise en place en automatisant les etapes a partir de la cible choisie. Ce sont d'assez ancien outils qui aujourd'hui souffrent de lacunes de part les technologies utilisees. Basés sur *Noble* et *Bleno*, des librairies en JavaScript basées sur NodeJS et permettant de manipuler le BLE, ils manque de flexibilité et ne permettent pas entre autre la coexistence d'appareils BLE, obligant l'utilisation de machine virtuelle pour chaque *dongle*. *Mirage* reprend le fonctionnement de ces outils, l'integrant en tant que module, mais basé sur de nouvelles librairies, notamment *PyBT*^[https://github.com/mikeryan/PyBT] permettant de simuler le comportement d'un appareil BLE en s'émacipant les contraintes imposees par leurs equivalent JavaScript, *Noble* et *Bleno*.

### Jamming
Le brouillage de communication est egalement une attaque assez populaire et implementee dans bon nombre d'outils sur le marché. Le but est de creer du bruit sur le canal au moment de la transmission pour corrompre le message, le rendant inutilisable par le recepteur. Concernant le BLE, *Ubertooth One* dispose des capacités nécessaire pour brouiller les canaux d'annonce ainsi qu'une communication etablie par retransmission simultanee. *BTLEJack* implemente egalement le brouillage au sein de son firmware personnalisé et, ayant deja un mecanisme permettant de se synchroniser avec une communication, peut egalement brouiller une communication etablie.

### Hijacking
Le principe est de voler une connexion entre 2 appareils en forcant une deconnexion de l'un pour prendre sa place. Cette nouvelle attaque, implementée par *BTLEJack* et reprise dans *Mirage*, utilise les différences de *timeout* entre le *Master* et le *Slave* pour forcer le *Master*, via l’utilisation de jamming sur les paquets du *Slave*, à se déconnecter et prendre ainsi sa place au sein de la communication.

## Mirage

Après comparaison entre les outils disponibles (voir @tbl:ble-tools), j'ai choisie *Mirage* car il dispose de la flexibilite voulue pour implementee des attaques scenarisee: acces aux couches bas niveau pour recuperer informations comme force du signal et calibrage (necessaires pour calculer la position d'un appareil lors de la localisation). Il dispose egalement d'une implementation d'un *Master* et *Slave* personnalisables pour realiser un reseau de tests sur lequel verifie l'implementation des attaques. Enfin, il supporte une varieté de composants matériel^[https://homepages.laas.fr/rcayre/mirage-documentation/devices.html] ainsi que toutes les attaques necessaires^[https://homepages.laas.fr/rcayre/mirage-documentation/modules.html] pour la preuve de concept, rendant le developpement plus simple.

Concernant le matériel necessaire a la preuve de concept il me faudra d'abors deux *dongles HCI* compatibles avec Mirage et supportant le changement d'adresse *BD* pour le *spoofing*. *Mirage* se base sur les numeros de constructeurs des *dongles* definit par le Bluetooth^[https://www.bluetooth.com/specifications/assigned-numbers/company-identifiers/] pour savoir s'ils sont compatibles. Il supporte une variete des constructeur dont le *CSR8510*^[https://www.qualcomm.com/products/csr8510] de Qualcomm, puce tres populaire dans les *dongles HCI* basiques et permettant le changement d'adresse *BD*.  
Concernant le *sniffer* necessaire pour la pupart des attaques, *Mirage* se basant sur *BTLEJack*, les cartes supportées par celui-ci le sont aussi par *Mirage*. Même si *Mirage* supporte d'autres cartes comme celles de developpement de *Nordic Semiconductor* ou l'*Ubertooth One*, elles ne sont pas adaptées pour mon projet car trop cher pour les fonctionnalités exploitees dans la preuve de concept.  
Je me suis donc tourné vers les cartes compatibles avec *BTLEJack*^[https://homepages.laas.fr/rcayre/mirage-documentation/devices.html#btlejack-device]. *Bluefruit* d'Adafruit, Waveshare *BLE400*^[https://www.waveshare.com/ble400.htm] et les kits *nRF51*^[https://www.waveshare.com/nrf51822-eval-kit.htm] demandent une reprogrammation via un peripherique externe utilisant le port *SWD*. Ne disposant pas du materiel necessaire pour la reprogrammation et celui-ci etant assez onéreux, j'ai choisit la *BCC Micro:Bit*, carte avec lequel *BTLEJack* à ete originalement developpé.

TODO tableau comparatif technologies

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