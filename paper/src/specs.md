```{=latex}
\clearpage
```

# Preuve de concept

Sujet: Étudier puis mettre en place des attaques sur le protocole *Bluetooth Low Energy* (également appelé *Bluetooth Smart*).

Le but est d'exposer puis abuser des failles dans le protocole `BLE` 4.0 (première version). Ces failles sont connues et ont pour la plupart été corrigées dans les versions ultérieures du protocole (aujourd'hui en version 5.1). Néanmoins cela permet d'étudier et comprendre les mécanismes du BLE depuis sa création, puis voir les alternatives qui ont été proposées pour mitiger ces attaques.  
Je ne cible que les appareils supportant l'appairage en `BLE` 4.0 (dit *legacy*) avec méthode d'appairage *JustWorks*. C'est le niveau de sécurité minimal prit en charge par le protocole et très répandu dans les appareils connectés `BLE`. La majeure partie des appareils connectés sont simples, ne réalisant qu'une fonction d'augmentation, ne disposant ainsi pas de clavier ou d'écran et ne permettent donc pas l'utilisation de méthode d'appairage autre que *JustWorks*.  
Les mécanismes proposés à partir de la version 4.2 du `BLE` sont beaucoup plus robustes. Ils apportent une connexion securisée (*LE Secure Connections* ou `LESC`) se basant sur Diffie Hellmann pour l'échange de clefs ainsi qu'une nouvelle méthode d'appairage authentifiée (Comparaison numérique).

Même si le `BLE` à toujours proposé des mesures de sécurité, la majorité des constructeurs préfèrent mettre en place un chiffrement au niveau de la couche application (le `BLE` chiffre depuis la couche lien).  
Ces chiffrements propriétaires sont souvent basés sur des algorithmes reconnus comme `AES` et des méthodes telles *challenge-response* pour authentifier un appareil. Une clef unique est integrée dans chaque appareil, celle-ci sera soit distribuée au propriétaire de l'appareil lors de la création du compte ou le téléchargement de l'application associée, soit gardée par le constructeur qui transmettra directement les commandes depuis l'utilisateur à l'appareil (via l'application, ou directement si l'appareil est connecté au réseau mondial).  
Ces mécanismes exposent cependant beaucoup plus d'informations que le chiffrement `BLE`, réalisé depuis la couche lien. Les requêtes *ATT* et *GATT* transittent en clair et pour pallier à cette fuite d'informations les constructeurs évitent les requêtes standardisées dans le `BLE` et préfèrent utiliser des protocoles personnalisés dans la couche application, celle-ci étant chiffrée.  
Ces chiffrements propriétaires sur la couche application sont hors de portée de mon sujet mais ont fait couler beaucoup d'encre. Plusieurs présentations et leurs *whitepaper* sont disponibles dans des conférences de sécurité offensive comme *black hat*[@blackhat], *Defcon*[@defcon] ou encore *SSTIC*[@sstic].

Maintenant il s'avère que beaucoup d'appareils autonomes simples ne mettent aucune mesure de sécurité en place, quelles soient standardisées ou propriétaires, car les données qui transittent ne sont pas jugées sensibles. C'est notamment le cas des objets domotiques autonomes comme les télécommandes pour lampes dites connectées.

## Travail demandé

Mettre en place un outil basé sur un framework offensif permettant de répertorier et faciliter l'analyse des appareils et connexion `BLE` alentours. Cet outil est facilement portable sur diverses cartes de développement comme la `Raspberry Pi` car conteneurisé avec `Docker` et se basant sur du matériel USB pour l'étude du protocole.  
3 ports USB suffisent pour permettre de conduire toutes les attaques proposées par le framwork offensif utilisé: 2 dongles USB `BLE` 4.0 et une carte `BBC micro:bit`.  
Le projet suppose la mise en place de 3 attaques dont une nouvelle qui ne fait actuellement pas partie de `Mirage`:
- Inventaire des appareils et connexions à proximité + localisation des appareils (*scan* et *sniffing*)
- Usurpation et mise en place d'un *Man In The Middle* sur un appareil selectionné (*spoofing*)
- Synchronisation puis détournement par brouillage d'une connexion précédement identifiée (*hijacking*)

## Architecture

Le *back-end* en `python` permet le pilotage de `Mirage` via une interface logicielle (*Application Programmable Interface*, en rouge sur @fig:poc-arch). Cette *API* fait le lien entre le serveur `HTTP/Websocket` `Flask` (violet) et `Mirage` (bleu) qui pilote le matériel nécéssaire pour les attaques (vert). J'ai opté pour une interface web côté *front-end* car les technologies (surtout du `javascript`) ont explosées ces dernières années, rendant l'intégration d'intefaces plus simples et flexibles que les interfaces graphiques applicatives. Cette page se voulant un panneau de controle, un framework `javascript` (`Hyperapp`, en bleu clair) permet l'interactivité recherchée. Concernant les communications, il me fallait un protocole à double sens puisque l'on doit pourvoir suivre l'avancée d'une attaque en temps réel, ce que ne permet pas `HTTP`. Les *websockets* etant tres populaires dans les applications `javascript` comme les mini-jeux, jai intégré `Socket.IO` (jaune) en front et *back-end*: c'est une librairie de communication evenementielle basee sur les *websockets*. `Hyperapp` ou `Flask` souscrivent aux evenements de `Socket.IO` pour lancer des attaques sur `Mirage` ou modifier le `DOM` en adéquation (*Document Object Model*, c'est la vue `HTML` représentée en rouge sur @fig:poc-arch).

![Architecture du système](img/poc-arch.png){#fig:poc-arch}

## Interface

Elle sert de panneau de contrôle pour la supervisation du *scan* et *sniffing* des appareils et connexions alentours. Le but est d'augmenter `Mirage` avec une interface graphique (*Graphical Uuser Interface*) pour les attaques implémentées dans le projet. C'est un environnement plus familier que le terminal et ces ligne commandes (*Command Line Interface*), rendant plus accessible les démonstrations de sensibilisation.  
On retrouve les appareils et connexions identifiées par le *scan* sur la colonne de droite (@fig:front). La colonne de gauche est découpée en trois parties: les contrôles permettant de lancer ou interrompre une attaque, une carte affichant les appareils localisés ainsi que leur distance et les messages remontés par `Mirage` (*logs*).

![Interface du système](img/front.png){#fig:front width=100%}
