<!--
Le but est d'étudier l'architecture des systèmes domotiques sous l'angle de la sécurité pour chercher des possibles fuites d'informations ou compromossions possible.  
L'état de l'art révèle différentes architecture suivant le besoin et l'intégration voulue ainsi qu'une variété de canaux de communications plus ou moins adaptés.  
Je me focaliserait sur les architecture contenant un *hub* domotique reliant tout les appareils ainsi que le protocole de communication `Bluetooth` en mode `Low Energy` (`BLE`).  
Après étude de l'historique des attaques perpétuées sur le `BLE` et les objets domotique (connectés), je me consacrerait à la réalisation d'une preuve de concept sur des appareils `BLE`.
-->

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

# Architecture

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