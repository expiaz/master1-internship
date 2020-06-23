```{=latex}
\clearpage
```

# Preuve de concept

Sujet: Étudier puis mettre en place des attaques sur le protocole *Bluetooth Low Energy* (Bluetooth Smart)

Le but est d'exposer puis abuser des failles dans le protocole BLE 4.0 (première version). Ces failles sont connues et ont pour la plupart été corrigées dans les version ultérieures du protocole (aujourd'hui en version 5.1). Néanmoins cela permet d'étudier et comprendre les mécanismes du BLE depuis sa création, puis voir les alternatives qui ont étés proposées pour mitiger ces attaques.  
Je ne cible que les appareils supportant l'appairage en BLE 4.0 (dit *legacy*) avec méthode d'appairage *JustWorks*. C'est le niveau de sécurité minimal prit en charge par le protocole et très répandu dans les appareils connectés BLE. La majeure partie des appareils connectés sont simples, ne realisant qu'une fonction d'augmentation, ne disposant pas de clavier ou d'écran et ne permettent pas ainsi l'utilisation de méthode d'appairage autre que *JustWorks*.  
Les mécanismes proposés à partir de la version 4.2 du BLE sont beaucoup plus robustes. Ils apportent une connexion securisée (LE Secure Connections ou LESC) se basant sur Diffie Hellmann pour l'échange de clefs ainsi qu'une nouvelle méthode d'appairage authentifiée (Comparaison numérique).

Même si le BLE à toujours proposé des mesures de sécurité, la majorité des constructeurs ne les utilisent pas et mettent en place des chiffrements au niveau de la couche application (le BLE chiffre depuis la couche lien).  
Ces mesures de sécurité propriétaires sont souvent basées sur des algorithmes reconnus comme AES et des methodes telles *challenge-response* pour authentifier un appareil. Une clef unique est integrée dans chaque appareil, celle-ci sera soit distribuée au proprietaire de l'appareil lors de la création du compte ou le téléchargement de l'application associée, soit gardée par le constructeur qui transmettra directement les commandes depuis l'utilisateur à l'appareil (via l'application ou directement, si l'appareil est connecté au réseau mondial).  
Ces mécanismes exposent cependant beaucoup plus d'informations que le chiffrement BLE depuis la couche lien. Les requêtes *ATT* et *GATT* transittent en clair et pour pallier à cette fuite d'informations les constructeurs évitent les requêtes standardisées dans le BLE et préfèrent utiliser des protocoles personnalisés dans la couche application, celle-ci étant chiffrée.  
Ces chiffrements propriétaires sur la couche application sont hors de portée de mon sujet mais ont fait couler beaucoup d'encre. Plusieurs présentations et leurs *whitepaper* sont disponibles dans les conférences *black hat*^[https://www.blackhat.com/], *Defcon*^[https://www.defcon.org/] ou encore *SSTIC*^[https://www.sstic.org/].

Maintenant il s'avère que beaucoup d'appareils autonomes simples ne mettent en place aucune mesure de sécurité, qu'elle soit standardisée ou propriétaire, car les données qui transittent ne sont pas jugées sensibles. C'est notamment le cas des objets domotiques autonomes comme les télécommandes pour lampes dites connectées.

## Travail demandé

Mettre en place un outil basé sur un framework offensif permettant de répertorier et faciliter l'analyse des appareils et connexion BLE alentours. Cet outil est facilement portable sur diverses cartes de développement comme la Raspberry Pi car conteneurisé avec *Docker* et se basant sur du matériel USB pour l'étude du protocole.  
3 ports USB suffisent pour permettre de conduire toutes les attaques proposées par le framwork offensif utilisé: 2 dongles USB BLE 4.0 et une carte BBC Micro:bit.  
Le projet suppose la mise en place de 3 attaques dont une nouvelle non integrée à Mirage:
- Inventaire des appareils et connexions a proximité + localisation des appareils (*scan*)
- Usurpation et mise en place d'un *Man In The Middle* sur un appareil selectionné (*spoofing*)
- Synchronisation puis détournement par brouillage d'une connexion précédement identifiée (*hijacking*)

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

![Interface du système](img/front.png){#fig:front width=80%}
