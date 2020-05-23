<!--
Le but est d'étudier l'architecture des systèmes domotiques sous l'angle de la sécurité pour chercher des possibles fuites d'informations ou compromossions possible.  
L'état de l'art révèle différentes architecture suivant le besoin et l'intégration voulue ainsi qu'une variété de canaux de communications plus ou moins adaptés.  
Je me focaliserait sur les architecture contenant un *hub* domotique reliant tout les appareils ainsi que le protocole de communication `Bluetooth` en mode `Low Energy` (`BLE`).  
Après étude de l'historique des attaques perpétuées sur le `BLE` et les objets domotique (connectés), je me consacrerait à la réalisation d'une preuve de concept sur des appareils `BLE`.
-->

Dans le cadre du master CSSE nous etudions l'internet des objets (IoT) et leurs aspects securite. Le Bluetooth Low Energy (BLE) est une specification du protocole Bluetooth pour les objets fonctionnant sur batterie, visant notamment les objets connectes.  
Standardise, gratuit et integré dans la plupart des appareils de bureautique (laptop, smartphone) il est rapidement devenu populaire dans l'internet des objets.  
<!--
Le BLE repond aux nouvelles attentes pour l'internet des objets en etendant le Bt aux objets connectes. Le Bt a ete concus dans l'optique de creer des communications point a point WPAN (Wireless Personnal Area Network) entre des appareils de bureautique personnels (telephone, casque, ordinateur portable...).  
-->
La premiere iteration du BLE est principalement un portage du procole Bt vers une couche pysique "Low Energy". Celle ci integre des mesures de securite aujourd'hui desuetes et manque de fonctionnalites (topologies autres que point a point, localisation precise). Meme si le protocole a su evolue depuis pour repondre a ces besoins, beaucoup d'appareils *premiere generation* utilisent encore la version originale n'integrant pas encore ces mecanismes.  
Ce sont pour la plupart des appareils concus pour fonctionner en point a point avec un smartphone ou ordinateur comme les montres connectés, les capteurs corporels fitness, les termometres, serrures ou cadenas, etc. Les donnees personnelles peuvent etres interceptees et les actions modifiees (ouverture de cadenas, par exemple).

# Objets connectés

histoire des objets connectes
apparition objets intelligents (difference)
chiffre explosion depuis quelques annees

Apparition objets "augmentés" dits connectes (ou *smart* en anglais)

Avec l'explosion de l'internet de objets (TODO chiffres) la domotique est devenue accessible et s'est popularisée à travers les objets connectés. Ceux-ci étendent leur équivalent mecanique en integrant des composants electroniques, permettant le controle a distance par exemple.  

Tout une floppée d'objets du quotidien ont étés augmentés pour permettre la communication avec d'autres systemes informatique (les smartphones notamment).

Cependant ces améliorations engendrent une augmentation de la surface d'attaque: les objets connectés sont confrontés aux memes challenges que ceux des systèmes informatiques traditionnels en plus de leur fonction primaire.  

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

## Appareil standalone / augmenté
Architecture reseau domotique
- simple: appareil non relie au reseau, dependant gateway utilisateur, remplissant une fonction d'augmentation seul (smart lock)

## Reseau domotique / reseau capteurs
- avancee: appareil s'appuyant sur un reseau domotique pour realiser ses fonctions, relie a une gateway "sure" hub

## Protocoles

Protocoles generaux supportes par tout appareil (smartphone notamment) et peu cher
WiFi (WLAN) ~ Local = remplace cables pour appareils fixes dans pieces / appart
BLE (WPAN) ~ Personnal = remplace cables pour appareils portable personnels
NFC

Protocoles specifiques concus pour ces reseaux
Zigbee
Zwave
Thread
ANT(+)

## Marché

Premiere generation point a point "smart"

Seconde generation networks IoT

### Bt

Echange donnees

### BLE

Domotique

Gadgets

Entreprise / warehouse

smart city (tracking shopping)