```{=latex}
\clearpage
```

# Bluetooth Low energy

Le protocole a principalement été designé par Nokia pour répondre au besoin d'un protocole sans fil peu gourmand en énergie permettant la communication avec les périphériques personnels (téléphone portable, montre, casque audio). Nommé *Wibree*, il a été intégré au standard `Bluetooth` sous le nom *Low Energy*.  
Le `Bluetooth` ne comprend pas seulement un protocole mais une multitude d'entre eux (`BR`, `EDR`) qui ont en commun de permettre la communication (et l'échange de données) sans fil avec des périphériques personnels. Ils font partit des protocoles *WPAN* et leur distance d'émission varie de quelques mètres jusqu'à 30 mètres.  
La spécification `Bluetooth` 4.0, sortie en 2010, intégre le protocole `LE` (*Low Energy*) et permet au `Bluetooth` de toucher le marché des systèmes embarqués fonctionnants sur batterie.

## Différences

Les autres protocoles du `Bluetooth` sont principalement connus et utilisés pour le transfert de contenu multimédia, que ce soit des fichiers entre ordinateurs comme de la musique avec un casque ou encore une voiture. Ils fonctionnement avec une connexion continue et un transfert en mode flux.  
Le `BLE`, visant à reduire la consommation d'énergie, n'établie pas de connexion continue. L'appareil reste la plupart du temps en mode veille, pouvant émettre des annonces, dans l'attente d'une connexion qui aura pour effet d'arrêter la transmission d'annonces. Pour chaque requête reçu, une réponse pourra être renvoyée ou une notification mise en place périodiquement.  
Les appareils `BLE` et `Bluetooth BR/EDR` ne sont pas compatibles, n'utilisant pas les mêmes technologies/protocoles et répondant à des besoin différents (@tbl:bluetooth-use-case).

| **Besoin** | Flux données | Transmisson données | Localisation | Réseau capteurs |
| --- | --- | --- | --- | --- |
| **Appareils** | ordinateur, smartphone, casque, enceinte, voiture | accessoires bureautique ou fitness, équipement médical | beacon, IPS, inventaire | automatisation, surveillance, domotique |
| | | | | |
| **Topologie** | point à point | point à point | diffusion (1 à N) | mesh (N à N) |
| | | | | |
| **Technologie** | Bluetooth BR/EDR | Bluetooth LE | Bluetooth LE | Bluetooth LE |

: Cas d'utilisation et protocole Bluetooth adapté {#tbl:bluetooth-use-case}

## Protocole

Pour permettre une interopérabilité maximale entre les appareils `BLE`, le standard défini 4 profils en fonction du rôle de l'appareil: *Peripheral*, *Central*, *Broadcaster*, *Observer*. Chaque appareil se conformant au standard ne doit implémenter qu'un seul de ces rôles à la fois.  
Le *broadcaster* ne communique qu'avec des annonces, on ne peut pas s'y connecter. Ce mode est très populaire pour les balises (*beacons*). L'*observer* est sont opposé, il ne fait qu'écouter les annonces, n'établiera jamais de connexion.  
Le *peripheral* et le *central* forment la seconde paire et permettent la mise en place d'une architecture client-serveur. Le *peripheral* joue le rôle du serveur et est dit esclave du *central* qui endosse le rôle du client et maître.  
Le *peripheral* transmet des annonces jusqu'à recevoir une connexion d'un *central*, après quoi il arrête de s'annoncer car ne peut être connecté qu'à un *central* à la fois. Le *central* écoute les annonces de *peripheral* pour s'y connecter, puis interroge ses services via les requêtes *ATT/GATT*.

### Couche physique

Le `BLE` opère dans la bande ISM 2.4GHz tout comme le `Wi-Fi`. Contrairement aux canaux `Wi-Fi` de 20MHz, le `BLE` découpe le spectre en 40 canaux de de 2MHz (plage de 2400 à 2480MHz).  
Le protocole met en place le *saut de fréquence* qui consiste à changer de canal d'émission tout les laps de temps donné pour réduire le risque de bruit sur les fréquences utilisées (la bande ISM 2.4Ghz étant libre d'utilisation).  
Sur les 40 canaux que compose le spectre, 3 sont utilisés pour la transmission d'annonce. Ils sont choisit pour ne pas interférer avec les canaux `Wi-Fi` car les deux protocoles sont amenés à coexister (@fig:ble-channels).  
Les 37 autres canaux sont utilisés pour les connexions. Chaque connexion va utiliser un sous-ensemble des 37 canaux (appelé carte des canaux) pour éviter les interférences avec les autres protocoles et connexions `BLE`. Un seul canal transmet des données à la fois mais tous les canaux de la carte sont utilisés pour le saut de fréquences.

![Répartition du spectre BLE en canaux[@ble-chan]](img/ble-chan.jpg){#fig:ble-channels width=90%}

### Couche logique

![Étapes d'un échange BLE](img/ble-conn.png){#fig:ble-conn width=70%}

#### 1. Annonces

Le *peripheral* indique sa présence avec des annonces émises périodiquement. Ces annonces contiennent sont addresse Bluetooth (permettant une connexion) et des données qui consituent un profile (appelé *GAP*[@gap]). Ces données permettent aux *centrals* de savoir si il est capable de réaliser les fonctionnalités recherchées.  
La spécification Bluetooth définit des profiles type pour des applications communes dans les appareils BLE[@gatt]. Cela inclus par exemple les capteurs corporels pour le sport, les capteurs médicaux de surveillance (pour les diabetiques notamment), la domotique (termomètres, lampes), etc.

Dans un environnement BLE, les *centrals* ne peuvent pas reconnaître leurs *peripherals* à part avec une addresse Bluetooth fixe, mécanisme de moins en moins utilisé car vulnérable à l'usurpation. Les *peripherals* générent donc des adresses aléatoires et l'identification se fait via les données du *GAP* contenues dans l'annonce. Ce mécanisme permet à n'importe quel *central* de s'appairer à n'importe quel *peripheral* proposant le profil recherché.  
Par exemple, une application de smartphone BLE pouvant gérer la température pourrait s'appairer et utiliser n'importe quel appareil BLE qui implémente le profil standardisé pour les termomètres dans le *GAP*.  
Les profils ne sont certes pas exhaustifs mais permettent une intégration fonctionnelle avec un maximum d'appreils et prévoient un moyen d'intégrer des données propriétaires non standardisées[@gap-prop].

#### 2. Connexion

Lorsqu'un *central* reçois une annonce d'un *peripheral* auquel il souhaite se connecter, il lui envoit une intention de connexion sur les canaux d'annonce. Ce message contient tout les paramètres communs pour établir une connexion sur les canaux de données: carte des canaux utilisés, temps entre chaque saut de fréquence, nombre de canaux sautés par saut, adresse unique de la connexion (appelée *Access Adress*).  
Ce message (nommé *CONNECT_REQ*) est crucial lors d'attaques car il permet la synchronisation avec une connexion pour l'écoute passive et est donc jugé sensible puisque transmit sur les canaux d'annonces avant la mise en place du chiffrement.

#### 3. Capacités

Le BLE voulant garder une interopérabilité maximale entre les appareils mais tout les appareils ne disposant pas des mêmes fonctionnalités embarqués, il est définit plusieurs méthodes d'appairage en fonction des capacités disponibles sur les deux appareils.  
Chaque appareil va transmettre ses capacités à l'autre ainsi que ses exigences sur la connexion à établir. Les capacités sont déduites des fonctionnalités présentes physiquement sur l'appareil et les exigences dépend de la version du procole actuellement supportée par celui-ci.  
Les exigences comprennent la protection aux attaques *MITM* par l'authentification de l'appairage, l'établissement d'une connexion sécurisée (*LE secure connection*), la mise en place d'une session (*Bonding*) pour une reconnexion future ainsi que l'utilisation d'un canal autre que le BLE (comme le *NFC*) pour la transmission de secrets menant au chiffrement (*Out Of Band* ou *OOB*).

| Capacité | Description |
| --- | --- |
| No input | pas la capacité d'indiquer *oui* ou *non* |
| Yes/No | mécanisme permettant d'indiquer *oui* ou *non* |
| Keyboard | claver numérique avec mécanisme *oui*/*non* |

: Capacités d'entrée possibles[@ble-caps] {#tbl:ble-input-caps}

| Capacité | Description |
| --- | --- |
| No output | pas la capacité de communiquer ou afficher un nombre |
| Numeric Output | peut communiquer ou afficher un nombre |

: Capacités de sortie possible[@ble-caps] {#tbl:ble-output-caps}

| | No output | Numeric output |
| --- | --- | --- |
| No input | NoInputNoOutput | DisplayOnly |
| Yes/No | NoInputNoOutput | DisplayYesNo |
| Keyboard | KeyboardOnly | KeyboardDisplay |

: Capacité d'entrées/sorties de l'appareil[@ble-caps] {#tbl:ble-io-caps}

#### 4. Appairage

En fonction des capacités et des exigences émises par chacun des appareils, une méthode d'appairage est sélectionnée (voir @tbl:ble-pairing-methods).

| | **DisplayOnly** | **DisplayYesNo** | **KbdOnly** | **NoIO** | **KbdDisplay** |
| --- | --- | --- | --- | --- | --- |
| **DisplayOnly** | JustWorks | JustWorks | PassKey | JustWorks | PassKey |
| **DisplayYesNo** | JustWorks | JustWorks | PassKey | JustWorks | PassKey |
| **KbdOnly** | PassKey | PassKey | PassKey | JustWorks | PassKey |
| **NoIO** | JustWorks | JustWorks | JustWorks | JustWorks | JustWorks |
| **KbdDisplay** | PassKey | PassKey | PassKey | JustWorks | PassKey |

: Méthode d'appairage utilisée en fonction des capacités échangées[@ble-pair-methods]{#tbl:ble-pairing-methods}

Je m'intéresse principalement à la methode *JustWorks*. C'est celle par défaut lorsque deux appareils ne disposent pas des capacités nécessaires pour une autre. Elle est notamment beacoup présente pour les objets connectés puisque n'intégrant pas de mécanismes pour un appairage plus complexe (claver ou écran).  
*Passkey* permet d'authentifier l'appairage pour se protéger des usurpations d'identité (*Spoonfing* et *MITM*) puisque partageant un secret via l'utilisateur (ou un autre canal dans le cas du *OOB*). *JustWorks* ne permet pas d'authentifier les appareils et le chiffrement est moins robuste que les autres méthodes mais permet tout de même d'établir une communication chiffrée.  

La méthode d'appairage choisie permet de transmettre un des matériel cryptographique: la clef temporaire (*Temporary Key*). Cette phase est plus ou moins sensible à l'écoute passive en fonction de la méthode d'appairage et des exigences émises lors de l'échange des capacités.  
*JustWorks* avec connexion BLE 4.0 (dite *legacy*) est le mode le plus sensible puisque la clef temporaire est tout simplement zéro, ne disposant pas de moyen de transmettre une donnée par autre voie, elle peut donc etre trouvee rapidement par *brute-force*.  
La connexion *LE secure*, introduite à partir de la version 4.2, utilise l'algorithme Diffie-Hellman sur courbes elliptiques (*ECCDH*) pour l'échange du matériel cryptographiques et est donc résistante à l'écoute passive (*eavesdropping*) mais toujours vulnérable à l'usurptation d'identité avec *JustWorks*.

#### 5. Chiffrement

L'établissement du chiffrement de la connexion est ensuite réalisé par dérivation de la première clef temporaire transmise via la méthode d'appairage choisie et d'autres matériel cryptographique échangés via le protocole BLE. La clef obtenue est dite court terme (*Short Term Key*) car elle ne sera utilisée que pour cette connexion et devra être re-générée à chaque nouvelle connexion.  
Il est cependant possible de mettre en place une session en stockant une clef partagée dite long term (*Long Term Key*) si cela à été exigé lors de l'échange des capacités. La clef long terme (*LTK*) est stockée et associée à l'appareil communiquant pour rétablir une connexion future sans avoir à refaire une phase d'appairage.

A partir de la comprehension actuelle du protocole BLE et du fonctionnement de l'appairage, il semble recommandé de mettre en place une connexion securisee des que possible. Il est également judicieux d'éviter la méthode *JustWorks* au maximum et stocker une session pour éviter de réitérer l'appairage.  
Cependant, il est assez simple de forger un échange de capacités pour rétrograder la connexion en *legacy* et forcer *JustWorks* via les capacités échangées. C'est pourquoi certains appareils attendent des capacites et exigences minimales pour établir une connexion, sans quoi celle-ci est avortée. C'est notamment le cas d'appareils propriétaires conçus pour fonctionner ensemble.

#### 6. Requêtes

Les échanges sont réalisés sur la base d'une architecture client-serveur. Le *central* (client) interroge le *peripheral* (serveur) avec le protocole *ATT* (*ATTribute Protocole*). Chaque requête mène soit à une réponse du serveur, soit à la mise en place d'une notification lors d'un évènemment (valeur changée ou disponible).  
Les requêtes et réponses possibles sont standardisées dans le *GATT* (*Generic ATTributes*) pour permettre une interoperabilité maximale entre les appareils (comme pour le *GAP*). *GATT* et *GAP* partagent les mêmes profiles, seul la structure change. Le serveur *GATT* peut être interrogé pour établir une liste exhaustive de toutes les fonctionnalités d'un appareil la ou le *GAP* choisit ce que contient l'annonce mais est limité par la taille du paquet (31 octets).

### GAP

Dans le cas des *Peripherals* et *Centrals*, le *GAP* est principalement utilisé pour établir un profil du *peripheral* permettant la décision de connexion de la part du *central*.  
Pour les *Boardcasters* et *Observers* il permet la communication unidirectionnelle (*Broadcaster* vers *Observer*) via les annonces, ceux-ci utilisant la diffusion plutôt qu'une connexion point à point. On retrouve cette utilisation pour les beacons publicitaires ou de localisation intérieur.

### GATT

Pour l'échange de données lors de connexion point à point, le *GATT* est utilisé en mode client-serveur. L'architecture du serveur *GATT* est en entonnoir, la plus haute couche s'appelle un *service*, il encapsule des *caractéristiques*, chacune contenant une *valeur* et un ou plusieurs *descripteurs* fournissants des informations additionnelles sur la valeur (voir @fig:ble-gatt-arch).  
À chacune de ses couches (service, caracteristique, valeur, descripteur) est attribué un identifiant unique appelé *handle*. La plage des indentifiant est partagée entre toutes les couches donc si un service a l'identifiant `0x01` aucun autre service/caracteristique/attribut/descripteur ne peut l'utiliser.

Un service correspond generalement a un profil (standardisé ou non) comme par exemple un termomètre. Ce service exposerait des caracteristiques comme la température ou l'humidité. Chacune de ces caracatéristique contient la valeur (donnée brute) et des descripteurs pour indiquer l'unité ou encore un facteur ou formule pour convertir la valeur donnée en résultat exploitable.

À moins de connaître exactement l'appareil et de l'interroger à l'aveugle via les *handles* (ce qui peut être le cas entre des appareils propriétaires), il faut procéder par étape en découvrant d'abors les services disponibles, puis chaque caractéristique par service et enfin les valeurs de celles-ci.  
Pour procéder à la découverte d'un appareil, le protocole *ATT* dispose d'un type de requête par couche à interroger (voir @fig:ble-gatt-arch). Une fois le service voulu trouvé (ou la cartographie totale de l'appareil realisée), on peut lire, écrire ou souscrire à des attributs directement par *handle*. Le *GATT* met en place un système de droits par attribut pour protéger la lecteur, l'écriture et la souscription par le client.

Le *GATT* définit égalemet des services standardisés appelés primaire et secondaire censés êtres présent sur tous les appareils BLE afin de connaître les fonctionnalités standardisées (service primaire) et propriétaires (service secondaire) de l'appareil. Comme les *handle* sont définies arbitrairement par le serveur *GATT*, les profils standards et leurs services/caractéristiques sont identifiés par un *UUID* standardisé identique dans tout les appareils BLE[@gatt-std-services].

![Client et serveur GATT[@ble-gatt-arch]](img/ble-gatt-arch.png){#fig:ble-gatt-arch width=90%}

## Évolution

Depuis sa première itération en 2010 dans la version `4.0` des spécifications Bluetooth le BLE a évolué pour intégrer des mesures de sécurité avec l'ajout des connexions sécurisées *LE* en `4.2` puis la diversification des topologies avec l'introduction du *mesh* pour les réseaux de capteurs en `5.0` et dernièrement l'amélioration de la localisation intérieur (*Indoor Positionning System*) pour une précision de l'ordre du centimètre grâce aux systèmes angle d'arrivée et de départ (*AOA/AOD*).