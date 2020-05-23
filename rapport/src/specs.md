# Spécifications

Sujet: Mettre en place des attaques sur le protocole Bluetooth Low Energy (Bluetooth Smart)

## Fonctionnalités

La preuve de concept devra fournir plusieurs fonctionnalités offensive qui sont décritent ci-après.

### Repérage

Inventaire des appareils et connexions BLE a proximité.

- Écoute des annonces sur les 3 canaux publicitaires pour récuperer les appareils emetteurs.
- Écoute des communications sur les 37 canaux de données pour répertorier les communication actives.

### Localisation

Localisation des appareils BLE alentours.

- Écoute passive des annonces pour extraire le calibrage du signal et calculer la distance à partir de la puissance du signal reçu.
- Si le calibrage n'est pas émit dans l'annonce, établissment d'une connexion pour récuperer la valeur si disponible.

Opération répétables autant de fois que voulu pour améliorer la precision de la localisation (minimum 3 mesures pour une position).

### Identification

Connexion directe à un appareil via son adresse bluetooth pour extraire toutes les données exposées.

- Écoute optionnelle des annonces pour identifier un esclave cible.
- Requête de connexion à la cible en tant que maître.
- Récupération des informations standardisées (GAP/GATT) ainsi que services et attributs propriétaires.

### Interception

Interception de communications et possible déchiffrement des trames.

- Écoute des communications sur les 37 canaux de données.
- Récupération de l'adresse d'accès et des paramètres d'appairage (carte des canaux, temps et nombre de sauts, etc).
- Synchronisation avec la communication et écoute des trames.
- Si la communication est chiffrée et la phase d'appairage passée, déconnexion des appareils via brouillage des communication jusqu'au temps mort.
- Écoute des canaux d'annonce: attente d'un appairage en supposant qu'il provienne des appareils precedement déconnectés.
- Récupération des informations cryptographique pour déchiffrer la connexion seulement si celle-ci n'utilise pas une clef a long terme deja établie ou une connexion securisée (BLE 4.2).
- Écoute des communications et déchiffrement des trames à la volée.

### Modification

Attaque *man in the middle* par clonage et usurpation d'un appareil BLE pour modifier les données echangées.

- Écoute passive des annonces de l'esclave cible de l'usurpation pour retransmission ultérieur et récupération de l'adresse bluetooth.
- Connexion à l'esclave cible d'usurpation pour qu'il n'émette plus d'annonces.  
- Changement de l'adresse de l'usurpateur en celle de l'esclave usurpé et réémission des annonces précédement capturées.
- Attente de la connexion du maître.
- Appairage entre l'usurpateur et le maître.
- Retransmission des communications entre le maître et l'esclave par l'usurpateur.

Il sera par la suite envisageable d'associer plusieurs fonctionnalités pour réaliser des scénarios différents. Ce peut être par exemple l'usurpation d'un appareil suite au brouillage lors de l'interception des communications entre 2 appareils.

## Architecture

Le système se compose d'un front-end fournissant une interface utilisateur affichant les appareils BLE et les actions possible ainsi qu'un back-end permettant la réalisation des actions implementées.

![Architecture du système](img/ubs.png)

## Interface

On retrouve la carte des appareils et connexions identifiés avec leur distance et position estimée par rapport à notre système.  


![Interface du système](img/ubs.png)

## Tests

Appareils necessaires pour tester le systeme
Precedure de test pour chaque fonctionnalite

## Livrables

- code source du système fonctionnel
Code source git + container docker pour tests et tout
- documentation du système
Une documentation developpeur du fonctionnement du framework ...
- rapport de projet
???