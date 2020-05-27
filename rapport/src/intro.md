Dans le cadre du master CSSE nous étudions l'internet des objets (IoT) et leurs aspects sécurité. Le protocole réseau sans fil Bluetooth Low Energy (BLE) permet une consommation réduite pour les objets fonctionnant sur batterie, visant notamment les objets connectés. Même si intégré à la spécification Bluetooth, il est incompatible avec les autres variantes de celui-ci.  
Aujourd'hui integré dans la plupart des appareils de bureautique, il est rapidement devenu populaire dans l'internet des objets.

La première itération du BLE (sortie en 2011) ne répond plus aux exigences de sécurité contemporaine et même si le protocole à su évoluer depuis pour repondre à ces besoins, beaucoup d'appareils utilisent encore la version originale n'intégrant pas ces mécanismes.  
Ce sont pour la plupart des appareils conçus pour fonctionner sur batterie et communiquer en point à point. On va retrouver les capteurs corporels pour santé ou fitness mais également des mecanismes plus sensibles tels des cadenas ou serrures. Les communications (incluant parfois des données personnelles) peuvent êtres interceptées, voir modifiées pour réaliser une action non voulue (ouverture de cadenas).

# Objets connectés

Avec l'explosion de l'internet de objets (TODO chiffres) toute une floppée d'objet du quotidien ont étés augmentés pour permettre la communication avec d'autres systemes informatique dont nos smartphones ou encore des serveurs distants (via notre WiFi). Ces objets dits intelligents étendent leur équivalent mécanique en intégrant des composants éléctroniques, permettant notamment le contrôle à distance.  
Cependant ces améliorations engendrent une augmentation de la surface d'attaque: les objets connectés sont confrontés aux mêmes challenges que ceux des systèmes informatiques traditionnels en plus de leur fonction primaire.  

TODO securite plus en plus pris en compte mais secondaire tj

<!--
# Domotique

Avec l'explosion de l'internet de objets (TODO chiffres) la domotique est devenue accessible et s'est popularisée à travers les objets connectés. Ceux-ci étendent leur équivalent mecanique en integrant des composants electroniques, permettant le controle a distance par exemple.  
Ces ameliorations engendrent une augmentation de la surface d'attaque car leur modèle de menace doit intégrer non seulement leur fontion primaire (serrure, lampe, ...) mais également les systèmes informatiques utilisé.  

Comme dans beaucoup de secteurs industriels, la sécurité n'est pas la priorité des fabriquants d'objets connectés. 
Ces appareils gerent des donnees utilisateur (personnelles) et leur utilisation pe critique (serrure, voiture).
Devices peu cher generalement, bcp market/hype (voir ces), securite sous cote (mm si mtn c gage qualite) car fct avant tout.

Les 

Ces ameliorations engendrent une augmentation de la surface d'attaque car ces *objets intelligents* (ou connectés) doivent résoudre les mêmes challenge que ceux des systèmes informatiques traditionnels en plus de leur fonction primaire.  
Ces ameliorations engendrent une augmentation de la surface d'attaque de par l'integration et la communication entre systemes informatiques.
explosion IoT, democratisation domotique, connexion de differents appareils (alexa, smartphone ,sensor, smart things).
Securite souvent sous estimee, protocoles non adaptes et solution mal implementee / configuree

-->

## Architecture

### Point à point
Architecture reseau domotique
- simple: appareil non relie au reseau, dependant gateway utilisateur, remplissant une fonction d'augmentation seul (smart lock)

### Réseau
- avancee: appareil s'appuyant sur un reseau domotique pour realiser ses fonctions, relie a une gateway "sure" hub

## Protocoles

Protocoles generaux supportes par tout appareil (smartphone notamment) et peu cher
WiFi (WLAN) ~50m: Local = remplace cables pour appareils fixes dans pieces / appart
BLE (WPAN) ~10m: Personnal = remplace cables pour appareils portable personnels
NFC 

Protocoles specifiques concus pour ces reseaux
Zigbee
Zwave
Thread
ANT(+)

## Marché

Premiere generation point a point "smart"

Seconde generation networks IoT

### BLE

Gadgets (fitness)

Domotique (IoT)

Entreprise / warehouse / smart city (beacons)