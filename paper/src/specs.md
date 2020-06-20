
# Preuve de concept

Sujet: Étudier puis mettre en place des attaques sur le protocole *Bluetooth Low Energy* (Bluetooth Smart)

Le but est d'exposer puis abuser des failles dans le protocole BLE 4.0 (première version). Ces failles sont connues et ont pour la plupart été corrigées dans les version ultérieures du protocole (aujourd'hui en version 5.1). Neanmoins cela permet d'etudier et comprendre les mecanismes du BLE depuis sa creation, puis voir les alternatives qui ont etes proposees pour mitigees ces attaques.  
Je ne cible que les appareils supportant l'appairage en BLE 4.0 (dit *legacy*) avec méthode d'appairage *JustWorks*. C'est le niveau de sécurité minimal prit en charge par le protocole et très répandue dans les appareils connectés. La majeure partie des appareils connectés sont simples, ne realisant qu'une fonction d'augmentation, ne disposant pas de clavier ou d'écran et ne permettent pas ainsi l'utilisation de méthode d'appairage autre que *JustWorks*.  
Les mecanisme proposees a partir de la version 4.2 du BLE sont beaucoup plus robustes. Ils apportent les connexion securisee (LE Secure Connections ou LESC) se basant sur Diffie Hellmann pour l'echange de clefs ainsi qu'une nouvelle methode d'appairage authentifiée (Comparaison numerique).

Meme si le BLE a toujours proposé des mesures de securité, la majorite des constructeurs ne les utilisent pas et mettent en place des chiffrements au niveau de la couche application (la ou le BLE chiffre depuis la couche lien).  
Ces mesures de securité proprietaires sont souvent basees sur des algorithmes reconnus comme AES et des methodes comme le *challenge-response* pour authentifier un appareil. Une clef unique est integrée dans chaque appareil, celle-ci sera soit distribuee au proprietaire de l'appareil lors de la creation du compte ou le telechargement de l'application associee, soit gardee par le constructeur qui transmettra directement les commandes de l'utilisateur a l'appareil (via l'application ou directement si l'appareil est connecté au reseau mondial).  
Ces mecanismes exposent cependant beaucoup plus d'informations que le chiffrement BLE depuis la couche lien. Les requetes ATT et GATT transittent en clair et pour pallier a la fuite d'informations les constructeurs evitent les requetes standardisee danas le BLE et preferent utiliser des protocoles personnalisés dans la couche application, celle-ci étant chiffrée.  
Ces chiffrements proprietaires sur la couche application sont hors de portee de mon sujet mais ont fait couler beaucoup d'encre et plusieurs presentation et leurs *whitepaper* sont disponibles.

Maintenant il s'avere que beaucoup d'appareils autonomes simples ne mettent en place aucune mesure de securite, qu'elle soit standardisee ou proprietaire, car les donnees qui transittent ne sont pas jugees sensibles. C'est notamment le cas des objets domotiques autonomes comme les telecommandes pour lampes dites connectées.

## Travail demandé

Mettre en place un outil basé sur un framework offsenf permettant de répertorier et faciliter l'analyse des appareils et connexion BLE alentours. Cet outil est facilement portable sur diverses cartes de developpement comme la raspberry Pi car conteneurisé avec *Docker* et se basant sur du materiel USB pour l'etude du protocole (dongle et sniffer).  
3 ports USB suffisent pour permettre de conduire toutes les attaques proposées par le framwork offensif utilisé (Mirage): 2 dongles USB BLE 4.0 et une carte BBC Micro:bit.  
Le projet suppose la mise en place de 3 attaques dont une nouvelle non integrée a Mirage:
- Inventaire des appareils et connexions a proximité + localisation des appareils (*scan*)
- Usurpation et mise en place d'un *Man In The Middle* sur un appareil selectionné (*spoofing*)
- Synchronisation puis detournement par brouillage d'une connexion precedement identifiée (*hijacking*)

## Architecture

serveur flask + websockets
application js (hyperapp) + socketio
framework offensif Mirage (python) + bindings custom pour communication API et non CLI

![Architecture du système](img/poc-architecture.png){#fig:poc-arch width=85%}

## Interface

But d'augmenter Mirage avec front-end pour demo et conduire attaques *type*

Technologie JS *Elm* (react trop lourd mais meme principe)

On retrouve la carte des appareils et connexions identifiés avec leur distance et position estimée par rapport au système (voir @fig:poc-ui: zone rouge *Scan*).  
Pour chaque cible (appareil ou connexion), des attaques sont disponibles:
- Récupération du profil ou modification des transimissions par usurpation pour un appareil BLE emettant des annonces (zone bleue *Devices*).
- Déconnexion des appareils ou interception des communications entre deux appareils appairés (zone bleue *Connections*).

TODO Screen GUI HTML
