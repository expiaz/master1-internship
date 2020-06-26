
# Étude de l'existant

## Outils

Les outils offensifs sur le protocole `BLE` permettent de récupérer, analyser et modifier les échanges entre appareils, ce qui permet de réaliser des audits de sécurité ou encore mettre en place des attaques pour exposer des vulnérabilités. L'analyse du traffic sans fil BLE demande une antenne couvrant la bande utilisee par les 40 canaux du protocole ainsi qu'un systeme assez rapide pour scanner puis suivre les communications lors des sauts de fréquence. Les radio-logiciels (*SDR*) ne sont donc pour la plupart pas adaptés car trop lents ou trop cher pour les fonctionnalités voulues: des outils spécialisés dans l'analyse et l'attaque du `BLE` sont disponibles pour une fraction du prix.

Le premier outil, utilisé dans tout nos appareils `BLE`, est la puce intégrée pour les communications `BLE`. Ces puces sont limités par un *firmware* spécifique qui ne permet pas la récupération (*sniffing*) et analyse ou modification d'un traffic sans fil, cela étant interdit. Même si il reste possible d'analyser le traffic entre la puce et un appareil `BLE` (notamment en utilisant *Wireshark*[@wireshark]), il n'est pas possible d'étendre les capacités de celle-ci sans modifier le *firmware*.  
Tout les appareils ne disposant pas d'une puce `BLE` dédiée, les constructeurs ont développés des *dongles* qui intègrent ces puces et permettent de communiquer avec tout appareil USB via une interface nommée *HCI* (*Host-Controller Interface*). Alliés aux outils standard du protocole `BLE` comme `BlueZ`, la pile protocolaire BLE du noyau Linux, ces *dongles* permettent de découvrir les appareils à proximité et d'endosser le rôle de *peripheral* ou *central* pour établir une communication avec n'importe quel autre appareil `BLE`. Les utilitaires `hcitool`, `hciconfig` et `gatttool` de `BlueZ` permettent par exemple de manipuler les annonces et extraire le profil *GATT* d'un appareil `BLE`. Même si certains de ces *dongles* proposent des fonctionnalités intéressantes comme le changement d'adresse `Bluetooth` (*Bluetooth Address* ou *BD*), ils n’ont pas été conçus dans une optique de sécurité, et sont peu flexibles pour un usage offensif.

La plupart des attaques sur le protocole `BLE` requièrent un moyen d'intercepter le traffic. Puisque les *dongles* et puces ne permettant pas cette fonctionnalité car destinés au grand public, plusieurs outils spécialisés ont emergés. On va retrouver des outils d'analyse de protocole sans fil généralistes comme la `HackRF` ou sa version spécialement conçue pour le BLE nommée `Ubertooth One`. Ces cartes sont assez cher mais hautement personnalisables depuis les couches bas niveau. Elles demandent un certain background de connaissances sur le protocole et les modulations sans fil pour arriver à un résultat précis comme la réalisation d'une attaque.  
Viennent ensuite les *sniffers* sous forme de dongle USB arrangés et plus ou moins personnalisables. Beaucoup sont basés sur les mêmes puces de *Nordic Semiconductor* ou *Texas Instrument* qui eux meme proposent leurs sniffers[@nrf-dongle;@ti-dongle] et logiciels[@nrf-soft;@ti-soft] pour l'analyse du protocole `BLE`. Dans les initiatives plus open-source, mais pas encore totalement personnalisable sans reprogrammation de la puce, on peut citer le `Bluefruit`[@bluefruit] de *Adafruit*.  
Enfin, un outils open-source appelé `BTLEJack`[@btlejack] permet non seulement l'étude mais également la mise en place d'une multitude d'attaques sur le protocole `BLE` via reprogrammation d'une carte de développement avec un *firmware* personnalisé. Cet outils à été développé pour la carte *BBC micro:Bit*[@microbit], une carte de developpement bon marché à but éducatif, puis porté sur plusieurs autres cartes intégrant une puce `nRF51` (notamment la `Bluefruit`).
Basé sur les travaux de `BTLEJack` et d'autres librairies `BLE` en `python`, `Mirage`[@mirage] permet des fonctionnalités identiques en supportant encore plus de cartes, de protocoles et d'attaques. Il comble le manque de flexibilité des précédents outils en intégrant plusieurs mécanismes qui permettent la mise en place d'attaques entièrement personnalisées, dites scénarisées, depuis les couches protocolaires basses et facilite l'ajout de fonctionnalités au sein du *framework*.

## Attaques

### Scanning
Le *scanning* consiste à répertorier des appareils BLE à proximité, on peut étendre l'inventaire aux connexions établies entre 2 appareils `BLE`. Là ou les *dongles HCI* suffisent pour intercepter les annonces diffusées, l'analyse des communications établies requiert un *sniffer* capable de suivre les 37 canaux de données.  
La pile protocolaire *BlueZ* permet le *scan* des *advertisements* (annonces) tandis que plusieurs outils precedements evoques comme `smartRF` ou `nRFSniffer` suffisent pour repérer une communication.

### Spoofing
C'est l'une des étape du *Man-In-The-Middle* qui permet d'usurper un *peripheral* `BLE`. Après identification de la victime (via annonces ou adresse *BD*), l'attaquant la clone en s'y connectant et extractant son profile *GATT*. L'attaquant peut rester connecté pour garder la victime silencieuse (un *peripheral* connecté n'émettant pas d'annonces) puis, via un *dongle HCI*, s'annonce comme étant l'appareil précédemment cloné.  
Cette attaque est réalisable en utilisant simplement un *dongle HCI* et l'utilitaire *BLueZ*. Les librairies et *frameworks* d'attaque discutés plus auparavant (*GATTAcker*, *BTLEJack*) intègrent également ces mécanisme.

### Sniffing
Le *sniffing* est l'analyse voir le suivis d'une connexion `BLE` (suivant les capacites du *sniffer* utilisé). Un premier cas de figure est l'attente d'une nouvelle connexion pour se synchroniser avec afin de suivre les échanges. La seconde option, et la plus courante, est la synchronisation avec une connexion auparavant établie: la difficulté ici réside en la récuperation des paramètres de connexion. Il est nécessaire de retrouver la carte des canaux utilisés (*channel map*) ainsi que le *hop increment* (nombre de canaux sautés) et *hop interval* (temps entre chaque saut) pour se synchroniser, sans quoi il est impossible de suivre une connexion à cause des sauts imprédictibles et trop fréquents.  
`BTLEJack`, et par conséquent `Mirage`, mettent en place un mécanisme permettant de retrouver ces informations de connexion à partir des échanges interceptés lors du *scanning*. Le *sniffing* de communications sans synchronisation quant à lui est une fonctionnalité très répandue et integrée à tout les sniffers `BLE` vu antérieurement.

### Man-In-The-Middle
L'attaque *Man-In-The-Middle* concerne n'importe quelle communication: l'attaquant peut modifier les échanges en venant se placer entre l'émetteur et le récepteur ciblé, se faisant passer pour l'un après de l'autre en usurpant leurs identités. Dans le cas du `BLE` on utilisera deux *dongles*, un pour usurpé le *peripheral* cible et un autre pour maintenir une connexion avec celui-ci. On doit d'abors usurpé le *peripheral* cible via du *spoofing* puis attendre la connexion d'un *central*. Une fois le *central* connecté à notre *dongle* usurpateur on se retrouve en situation de *Man-In-The-Middle* entre le *peripheral* et le *central*: on peut suivre et modifier le traffic avant de le retransmettre (@fig:mitm). A noté que l'on peut également usurpé le *central* si les appareils ciblés attendent un profil précis pour s'appairer.  

![Étapes d'une attaque *MITM*[@mirage-attacks]](img/mitm.png){#fig:mitm}

Plusieurs outils sont dediés à cette attaque car populaire et simple à mettre en oeuvre: `GATTAcker` et `BTLEJuice` facilitent la mise en place en automatisant les étapes à partir de la cible choisie. Ce sont d'assez ancien outils qui aujourd'hui souffrent de lacunes dûes aux technologies utilisées. Basés sur `Noble`[@noble] et `Bleno`[@bleno], des librairies `javascript` pour `NodeJS` et permettant de manipuler le `BLE`, ils manquent de flexibilité et ne permettent pas entre autre la coexistence d'appareils `BLE`, obligant l'utilisation de machine virtuelle pour chaque *dongle*[@mirage-paper]. `Mirage` reprend le fonctionnement de ces outils, l'intégrant en tant que module, mais basé sur de nouvelles librairies, notamment `PyBT`[@pybt] permettant de simuler le comportement d'un appareil BLE en s'affranchissant des contraintes imposées par leurs équivalent `javascript`, `Noble` et `Bleno`.

### Jamming
Le brouillage de communication est également une attaque assez populaire et implémentée dans bon nombre d'outils sur le marché. Le but est de créer du bruit sur le canal au moment de la transmission pour corrompre le message, le rendant inutilisable par le récepteur. Concernant le `BLE`, `Ubertooth One` dispose des capacités nécessaire pour brouiller les canaux d'annonce ainsi qu'une communication établie par retransmission simultanée. `BTLEJack` implémente également le brouillage au sein de son firmware personnalisé et, ayant déjà un mécanisme permettant de se synchroniser avec une communication, peut également brouiller une communication établie.

### Hijacking
Le principe est de voler une connexion entre 2 appareils en forcant une déconnexion de l'un pour prendre sa place. Cette nouvelle attaque, implémentée par `BTLEJack` et reprise dans `Mirage`, utilise les différences de *timeout* entre le *central* et le *peripheral* pour forcer le *central*, via l’utilisation de brouillage sur les paquets du *peripheral*, à se déconnecter et prendre ainsi sa place au sein de la communication.

## Mirage

Après comparaison entre les outils disponibles (@tbl:ble-tools), j'ai choisi `Mirage` car il dispose de la flexibilité voulue pour implémenter des attaques scénarisée: accès aux couches bas niveau pour récupérer dds informations comme force du signal et calibrage (nécessaires pour calculer la position d'un appareil lors de la localisation). Il dispose également d'une implementation d'un *central* et *peripheral* personnalisables permettant la mise en place d'un réseau de tests sur lequel vérifié l'implémentation des attaques. Enfin, il supporte une variété de composants matériel[@mirage-devices] ainsi que toutes les attaques nécessaires[@mirage-attacks] pour la preuve de concept, rendant le développement plus simple.

----------------------------------------------------------------------------------------------------------------------------------------------
Logiciel                *scan* *sniff* *mitm* *jam* *hijack* *locate*    Matériel
----------------------- ------ ------- ------ ----- -------- ----------- ---------------------------------------------------------------------
nRFSniffer              oui    oui     non    oui   non      non         puce `nRF51`

TIsmartRF               oui    oui     non    non   non      non         puce `CC25xx`

BTLEJuice               oui    non     oui    non   non      non         *dongle HCI* + `Bleno`/`Noble`

GATTAcker               oui    non     oui    non   non      non         *dongle HCI* + `Bleno`/`Noble`

BTLEJack                oui    oui     oui    oui   oui      non         `BBC micro:bit`, cartes basées sur puce `nRF51`

Mirage                  oui    oui     oui    oui   oui      possible    *dongle HCI*, `Ubertooth`, `nRF kit`, cartes compatibles avec `BTLEJack`
----------------------------------------------------------------------------------------------------------------------------------------------

: Comparaison des outils pour l'étude offensive du BLE {#tbl:ble-tools}

`Mirage` fournit des briques logicielles pour communiquer avec des appareils (*dongles*, *sniffers*) ainsi que décortiquer les protocoles, ce qui constitue le coeur du *framework*. Ces briques logicielles de base sont utilisées par des *modules* dans un but précis, par exemple réaliser le brouillage d'une communication `BLE`. `Mirage` fourni un certain nombre de modules qui mettent en place les attaques retrouvées dans les autres outils d'audit du `BLE` (`BTLEJack`, `GATTAcker`, ...) précédemment discutés. Similaire à la philosophie d'`Unix`, ces modules sont spécialisés dans une tàche précise et peuvent êtres assemblés entre eux pour réalisé des fonctionnalités plus complexes telle la connexion avec le module `ble_connect` puis l'extraction d'informations avec `ble_discover`. Enfin, il est possible de modifier les étapes d'une attaque via les *scénarios*: chaque module accepte un scénario surchargeant son flux d'exécution et ses méthodes.

Concernant le matériel necessaire, la preuve de concept nécessite d'abors deux *dongles HCI* compatibles avec `Mirage` et supportant le changement d'adresse *BD* pour le *spoofing*. `Mirage` se base sur les numéros de constructeurs des *dongles*, définit par le *Bluetooth SIG*[@ble-company-id], pour savoir s'ils sont compatibles. Il supporte une variété des constructeur dont le `CSR8510`[@csr8510] de Qualcomm (@fig:hci), puce très populaire dans les *dongles HCI* basiques et permettant le changement d'adresse *BD*.  
Concernant le *sniffer* nécessaire pour la pupart des attaques, `Mirage` se basant sur `BTLEJack`, les cartes supportées par celui-ci le sont également. Même si `Mirage` supporte d'autres cartes comme des kits de développement de *Nordic Semiconductor* ou l'`Ubertooth One`, elles ne sont pas adaptées pour mon projet car trop onéreuses pour les fonctionnalités exploitées dans la preuve de concept.  
Je me suis donc tourné vers les cartes compatibles avec `BTLEJack`[@mirage-btlejack]. `Bluefruit` d'Adafruit, Waveshare `BLE400`[@ble400] et les kits `nRF51`[@nRF51] demandent une reprogrammation via un périphérique externe utilisant le port *SWD*. Ne disposant pas du matériel nécessaire pour la reprogrammation, et celui-ci étant assez onéreux, j'ai choisit la `BCC micro:bit` (@fig:microbit): carte avec laquelle `BTLEJack` a été originalement développé.

```{=latex}
\begin{figure}
\centering
\begin{minipage}{.5\textwidth}
  \centering
  \includegraphics[width=.5\linewidth]{img/microbit.jpg}
  \captionof{figure}{Carte BBC micro:bit}
  \label{fig:microbit}
\end{minipage}%
\begin{minipage}{.5\textwidth}
  \centering
  \includegraphics[width=.5\linewidth]{img/hci.jpg}
  \captionof{figure}{Dongle HCI BLE CSR8510}
  \label{fig:hci}
\end{minipage}
\end{figure}
```
<!--
![carte BBC micro:bit](img/microbit.jpg){#fig:microbit width=30%} ![dongle HCI BLE CSR8510](img/hci.jpg){#fig:hci width=30%}
-->

### Intégration

`Mirage` est un "*framework offensif pour l'audit des protocoles sans fil*"[@mirage]. Il a été pensé pour le *pentest* (audit de sécurité) donc un usage exclusivement en ligne de commandes (*CLI*). Mème si le framework se veut beaucoup plus modulaire et extensible que ces prédécesseurs (`BTLEJack` notamment), cette modularité est exclusive à l'interface en ligne de commandes pour laquelle il est pensé.  

Le fait de devoir l'intégrer dans un *back-end* suppose une *API* pour communiquer avec `Mirage` depuis `Flask`. Ne disposant pas nativement de cette *API* je l'ai créée en m'inspirant de celle du *CLI*: j'ai repris la méthode d'initialisation du framework mais est remplacé les arguments en ligne de commande par une instanciation et hydratation des modules manuelle.  
Le *framework* est fait pour fonctionner le temps d'une attaque, après quoi il s'auto-termine, et compte sur le nettoyage par le système d'exploitation suite à la fin d'exécution de son processus pour fermer les *sockets* ou vider les files (*FIFO*) utilisées dans la communication avec le matériel par lien série. Dans cette philosophie j'ai été amené à combler ce manque car mon processus `python` est hôte de `Mirage`, il ne se ferme pas à la fin d'une attaque, retrouver un etat stable apres une attaque est donc primordial. Cela demande la suppression des caches utilisés dans l'instance de `Mirage`, fermeture des *socket* et synchronisation des fils d'exécutions (*threads*) qui supervisent le matériel, pour ne pas remplir les files alors que l'attaque est terminée.

Si cela peut avoir du sense de faire une interface pour superviser une nouvelle attaque ajoutée à `Mirage`, reconduire le fonctionnement et interactions des attaques d'ores et déjà disponibles via le *CLI* vers un *GUI* est discutable. Le *MITM* et *hijacking* sont des attaques interactives: après usurpation d'un appareil dans le *MITM*, l'utilisateur peut modifier à la volée les paquets échangés ou communiquer via un terminal avec le *peripheral* lorsque qu'une connexion à été détournée avec du *hijacking*. Cette interaction n'est reproductible qu'en imittant un terminal sur l'interface, ce qui revient a recréer l'interpréteur déjà intégré à `Mirage` pour n'ajouter qu'un peu de commodité à l'utilisateur (qui n'a pas à devoir utiliser le *CLI* depuis le conteneur `Docker`).

`Mirage` utilise des délais d'attente (`wait`, `sleep`) dans le processus principal pour attendre une certaine trame ou qu'un appareil soit dans l'état voulu. L'interactivité est conservée par des mises à jour periodique de l'avancée de l'attaque soit via des tableaux contenant les informations trouvées soit des messages indiquant un événement précis. Pour garder cette même interactivité dans le *front-end* durant l'exécution d'une attaque est plus complexe car la librairie `Socket.IO` dans le *back-end* ne se base non pas sur des fils d'exécution mais une boucle d'événements (principe utilisé dans `NodeJS` et popularisé par le `javascript`). Les événments lents comme les interactions avec le réseau sont toujours différées car le fil d'exécution principal est lui meme interrompu par de multiples délais d'attentes. En conséquence `Socket.IO` ne transmet jamais les événements et le *front-end* reste figé. Pour remédier à cela il à d'abors fallut rendre `Mirage` compatible avec le système de boucle d'événements, solution fournie par `Socket.IO` (qui plus est sans modifier le code du *framework*) par le remplacement des méthodes standard de suspension du fil d'éxécution (`sleep`, `wait`) avec leurs équivalents en boucle d'événements. Ensuite, plutôt que de lancer l'instance de `Mirage` sur son propre fil d'exécution, on l'insert dans la boucle d'événements qui supervise tout le *back-end*. Les fils d'exécution crées par `Mirage` suspendent ainsi son événement dans la boucle et non le fil d'exécution de la boucle d'événement lors d'appels a `sleep` et `wait`.
