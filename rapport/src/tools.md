
# Étude de l'existant

## Outils

Les outils offensifs sur le protocole BLE permettent de recuperer, analyser et modifier les echanges entre appareils permettant de realiser des audits de securite ou mettre en place des attaques exposant des vulnerabilites. L'analyse du traffic sans fil BLE demande une antenne couvrant la bande utilisee par les 40 canaux du protocole ainsi qu'un systeme assez rapide pour scanner puis suivre les communications lors des sauts de frequence. Les radio-logiciels (*SDR*) ne sont donc pour la plupart pas adaptés car trop lents ou trop cher pour les fonctionnalités disponibles: des outils specialises dans l'analyse et l'attaque du BLE sont disponibles pour une fraction du prix.

Le premier outil, utilisé dans tout nos appareils BLE, est la puce intégrée pour les communications BLE. La recuperation (*sniffing*) et analyse ou modification d'un traffic sans fil etant interdit, ces puces utilisent un *firmware* proprietaire ne permettant que la communication en *master* ou *slave* et respectant les specifications BLE. Même si il reste possible d'analyser le traffic (notamment en utilisant *Wireshark*^[https://www.wireshark.org/]) entre la puce et un appareil BLE, il n'est pas possible d'etendre les capacites de celle-ci sans modifier le *firmware*.  
Tout les appareils ne disposant pas d'une puce BLE dédiée, les constructeurs ont developpes des *dongles* integrant ces puces et permettant de communiquer avec tout appareil USB via une interface nommée *HCI* (*Host-Controller Interface*). Allié aux outils standard du protocole BLE comme *BlueZ*, la pile protocolaire BLE du noyau Linux, ces *dongles* permettent de découvrir les appareils a proximité et d'endosser le role d'esclave ou maitre pour etablir une communication avec n'importe quel autre appareil BLE. Les utilitaires *hcitool*, *hciconfig* et *gatttool* de *BlueZ* permettent par exemple de manipuler les annonces et extraire le profil *GATT* d'un appareil BLE. Meme si certains de ces *dongles* proposent des fonctionnalites interessantes comme le changement d'adresse Bluetooth, ils n’ont pas été conçus dans une optique de sécurité, et sont peu flexibles pour un usage offensif.

La plupart des attaques sur le protocole BLE requierts un moyen d'intercepter le traffic. Les *dongles* et *puces* embarquants des firmware ne permettant pas cette fonctionnalite puisque destines au grand public, beacoups d'outils specialises ont etes developpes. On va retrouver des outils d'analyse de protocole sans fil generaux comme la *HackRF* ou sa version specialement concue pour le BLE nommée *Ubertooth One*. Ces cartes sont assez cher mais hautement personnalisables depuis les couches bas niveau. Elles demandent un certain background de connaissances sur le protocole et les modulations sans fil pour arriver a un resultat precis (comme la realisation d'une attaque).  
Viennent ensuite les *sniffers* sous forme de dongle USB arrangées et plus ou moins personnalisables. Beaucoup sont basés sur les memes puces de *Nordic Semiconductor* ou *Texas Instrument* qui eux meme proposent leurs sniffers[^nrf-dongle][^ti-dongle] et logiciels[^nrf-soft][^ti-soft] pour l'analyse du protocole BLE. Dans les initiatives plus open-source, mais pas encore totalement personnalisable sans reprogrammation de la puce, on peut citer le Bluefruit^[https://www.adafruit.com/product/2269] de *Adafruit*.  
Enfin, un outils open-source nommé *BTLEJack* permet non seulement l'etude mais la mise en place d'une multitude d'attaques sur le protocole Ble via reprogrammation de la carte avec un firmware personnalisé. Cet outils a ete developpe pour la carte *BBC Micro:Bit*^[https://microbit.org/], une carte de developpement bon marché a but educatif, et est aujourd'hui compatible avec plusieurs autres cartes intégrant la puce `nRF51` (notamment la *Bluefruit*).
Basé sur les travaux de *BTLEJack* et d'autres librairies BLE en python, *Mirage*^[https://homepages.laas.fr/rcayre/mirage-documentation/index.html] permet des fonctionnalités identiques en supportant encore plus de cartes, de protocoles et d'attaques. Il comble le manque de flexibilité des precedants outils en integrant plusieurs mecanismes permettant la mise en place d'attaques scénarisées entierement personnalisees depuis les couches protocolaires basses et facilite l'ajout de fonctionnalités au sein du framework.

[^nrf-dongle]: https://www.nordicsemi.com/Software-and-tools/Development-Kits/nRF51-Dongle
[^ti-dongle]: http://www.ti.com/tool/CC2540EMK-USB
[^nrf-soft]: https://www.nordicsemi.com/Software-and-tools/Development-Tools/nRF-Sniffer-for-Bluetooth-LE
[^ti-soft]: http://www.ti.com/tool/PACKET-SNIFFER

tableau recap ?

## Attaques

### Scanning
Le *scanning* consiste à répertorier des appareils BLE à proximité. Dans le cas d'attaque on etendra l'inventaire avec les connexion établies entre 2 appareils BLE. Là ou les *dongles HCI* suffisent pour intercepter les annonces diffusées, l'analyse des communications établies requiert un *sniffer* capable de suivre les 37 canaux de données.  
La pile protocolaire *BlueZ* permet le *scan* des *advertisements* (annonces) tandis que plusieurs outils precedements evoques comme *smartRF* ou *nRFSniffer* suffisent repérer une communication.

### Spoofing
C'est l'une des étape du *Man-In-The-Middle* qui permet d'usurper un esclave BLE. Après identification de la victime (via annonce ou adresse BD), l'attaquant la clone en s'y connectant et extractant son profile *GATT*. L'attaquant peut resté connecté pour garder la victime silencieuse (un esclave connecté n'emettant pas d'annonces) puis, via un second *dongle* BLE, s'annonce comme étant l'appareil precedemment cloné.  
Cette attaque est realisable en utilisant simplement un *dongle HCI* et l'utilitaire *BLueZ*. Bien sur, les librairies et frameworks d'attaque discutés plus auparavant (*BTLEJack*, *Mirage*) integrent egalement ces mecanisme.

### Sniffing
Le *sniffing* est l'analyse voir le suivis d'une connexion BLE (suivant les capacites du *sniffer* utilisé). Un premier cas de figure est l'attente d'une nouvelle connexion pour se synchroniser avec afin de suivre les echanges. La seconde option, et la plus courante, est la synchronisation avec une connexion deja etablie: la difficulté ici réside en la recuperation des parametres de connexion. Il est necessaire de retrouver la carte des canaux utilisés (*channel map*) ainsi que le *hop increment* (nombre de canaux sautés) et *hop interval* (temps entre chaque saut) pour se synchroniser sans quoi il est impossible de suivre une connexion car les sauts trop frequents.  
*BTLEJack*, et par conséquent *Mirage*, mettent en place un mecanisme permettant de retrouver ces informations de connexion a partir des echanges interceptés lors du *scanning*. Le *sniffing* de communications sans synchronisation quant a lui est une fonctionnalité très répandue et integrée a tout les sniffers BLE vu antierieurement.

### Man-In-The-Middle

outils specialisés GATTAcker BTLEJuice, BTLEJack/Mirage reprennent fonctionnement sans lacunes haut niveau 

### Jamming
explication
Ubertooth BTLEJack nRF51

### Hijacking
explication
BTLEJack