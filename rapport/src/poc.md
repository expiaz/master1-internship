
# Preuve de concept

## Sniffing

## Localization

### Fingerprinting

A partir d'une liste de beacons et leurs position, calcul la position se rapprochant le plus d'un des beacons (a partir du RSSI).

Demande de pouvoir etablir la liste des beacons et les identifies de facon sure. Si le systeme est mit en place pour cet effet on s'assurera qu'ils soient identifiables (MAC unique par exemple) mais dans notre cas de recuperation d'information, les appareils peuvent mettre en place des mesures contre le tracage comme la generation d'adresse mac aleatoire.
Il est possible d'utiliser le profile GATT pour identifier un appareil, combiner avec le RSSI dans le temps et les deplacements (capteurs) on peut esperer distinguer deux profils GATT identiques.

~ beacons coverage

Le beacon le plus proche

### RSSI / TOA

~ m

Trilateration determines the position of an object
by understanding its distance from three known
reference points. In the case of Bluetooth, locators
estimate their distance to any given asset tag based
on the received signal strength from the tag

### AOA / AOD

~ cm

Basee sur le nouveau systeme d'angle du BLE 5.1
Demande du materiel en plus (Multiple antennes directionnelles pour former une matrice)
Differentes facon de calculee (angle arrivee, angle depart ...)

https://www.bluetooth.com/blog/bluetooth-positioning-systems/
https://www.bluetooth.com/bluetooth-resources/enhancing-bluetooth-location-services-with-direction-finding/?utm_campaign=location-services&utm_source=internal&utm_medium=blog&utm_content=bluetooth-positioning-systems


### Ajouter de la precision

Fusionner les resultats avec un filtre kalmann:
- dead reckoning
- trilateration / triangulation

Ou RSS (range) + AOA (direction)

### RSS

1. Scan devices
   BTLEJack sniffer
2. find settings (rssi, txPower / measured power ...)
   Tx Power service 0x1804 and Tx Power Level Characteristic 0x2A07
3. calculate distance (in a circle around you)
   10 ^ ((txPower – RSSI)/(10 * N))
   N = loss factor (between 2 and 4), 0 for optimal conditions
4. cross multiple references to determine a position (trilateration)
   repeat 3 times to 3 devices
   get OUR position

### AOA

## MITM
