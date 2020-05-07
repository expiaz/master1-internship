
# Attaque matos

## Logiciels

Etude des communications bluetooth:
Wireshark
Scappy
etc
Possible avec n'importe quel chip Bt deja sur la machine ou dongle USB pour une etude du traffic interne et des appareils emettants des adv.

Interceptions des communications
- BTLE (C)
- BTLEJack (lib python + firmware C)
- Mirage (framework python)

Proprietaires:
- nRF sniffer
- nRF Connect
- smartRF (TI)

Attaques
- GATTacker (NodeJS) MiTM
- BTLEJuice (NodeJS) MiTM
- BTLEJack (Jamming/ Hijacking)
- Mirage (MiTM / jam / hijack / crack)


## Materiels

We can BLE dedicated devices to sniff or modify it. Internal Bt chips can only adv or connect to peripherals but never scan or modify it. They only see internal traffic (locked firmware).

Full featured
HackRF
PandwaRF
Ubertooth

BLE HCI Dongle
nRF52840 (https://www.nordicsemi.com/Products/Low-power-short-range-wireless/nRF52840)
- https://www.nordicsemi.com/Software-and-tools/Development-Kits/nRF52840-Dongle
Some using CSR8510 (https://www.qualcomm.com/products/csr8510)
- Adafruit Bluetooth 4.0 USB Module (https://www.adafruit.com/product/1327)
- https://www.amazon.co.uk/CSR8510-Bluetooth-Adapter-Classic-Headset/dp/B01G92CNY8

Qualcomm, Broadcom, Realtek, NordicSemiconductor ...
Featured in documentation is Qualcomm one

Sniffer
- Ubertooth One ($$)
- BTLEJack BBC Micro:Bit, Bluefruit, Waveshare BLE400, nRF51822 Eval kit (tweak) (https://github.com/virtualabs/btlejack)
- Bluefruit https://www.adafruit.com/product/2269 (limited)
- nRF51 https://www.nordicsemi.com/Software-and-tools/Development-Kits/nRF51-Dongle (close)
- TI CC2540 USB Dongle BLE sniffer (http://www.ti.com/tool/CC2540EMK-USB)
- Crazy Radio PA 2.4GHz (https://store.bitcraze.io/collections/kits/products/crazyradio-pa)

Board
- HackRF
- PandwaRF

# Integration avec Mirage

Si je me concentre sur Mirage, cela restreint pas mal les outils possible:
- dongle BLE HCI standard
- sniffer BLE adaptable avec BTLEJack (micro:bit, bluefruit, ble400, nRF51)
Les appareils dépendent des besoin, dans mon cas il me faudrait:
- inventaire: Sniffer (BTLEJack)
- obtention d’informations (crack, mit): dongle HCI x2 (un slave et un master, a voir si un BTLEJack peut remplacer un HCI)
- localisation / tracking (rssi + autres méthodes): Mirage ne permet pas cela nativement mais les informations demandées doivent être récupérables dans le framework pour l’implementer manuellement (RSSI, angle antenne ?). Cela demande au minima un dongle HCI, meme si les travaux trouvés sur le sujet utilisent un sniffer Bluefruit.
Dans les travaux étudiés, la localisation demande 3+ appareils BLE pour permettre la trilatération

Il me manque donc a voir si un BTLEJack peut remplacer un HCI dans l’attaque MITM, ainsi que trouver des informations pour implementer la localisation IPS avec Mirage.
Mirage supporte également d’autres appareils (comme Ubertooth) mais leurs fonctionnalités ne nous sont pas nécessaires, un sniffer flashé avec BTLEJack suffit (et coute moins cher).
Pour les sniffers BTLEJack eligibles:
- Bluefruit et nRF51 (~20e) demandent reprogrammation via un “external SWD” (assez cher + 100e)
- la carte BBC Micro:bit (20e, non vendue en France directement) permet une reprogrammation sans appareil supplémentaire, et semble donc la plus simple

Pour résumer:
- dongle BLE (https://www.adafruit.com/product/1327 / https://www.amazon.co.uk/CSR8510-Bluetooth-Adapter-Classic-Headset/dp/B01G92CNY8)
- carte Micro:Bit (https://microbit.org/buy/)

# Utilisation Mirage

## Sniffing

## Localization

## MITM

HCI dont au moins 1 reprogrammable @BD, capa necessaires:
```python
# mirage/modules/ble_mitm.py:14
def checkCapabilities(self):
    a2scap = self.a2sEmitter.hasCapabilities("COMMUNICATING_AS_MASTER","INITIATING_CONNECTION","SCANNING")
    a2mcap = self.a2mEmitter.hasCapabilities("COMMUNICATING_AS_SLAVE","RECEIVING_CONNECTION","ADVERTISING")
    return a2scap and a2mcap
```

HCI Capa:
```python
# mirage/libs/ble.py:125
self.capabilities = ["SCANNING", "ADVERTISING", "INITIATING_CONNECTION", "RECEIVING_CONNECTION", "COMMUNICATING_AS_MASTER", "COMMUNICATING_AS_SLAVE"]
```

BTLEJack capa:
```python
# mirage/libs/ble_utils/bltejack.py:1156
self.capabilities = ["SNIFFING_EXISTING_CONNECTION", "SNIFFING_NEW_CONNECTION", "HIJACKING_CONNECTIONS", "JAMMING_CONNECTIONS", "COMMUNICATING_AS_MASTER"]
```

BTLEJack n'a ni les capa necessaires pour run en slave ni en master (seul `COMMUNICATING_AS_MASTER`), de plus il aurait fallut qu'il run en master (a2scap) car le slave (a2mcap) doit pouvoir changer son @BD et seul les device HCI peuvent (implem dans `BtHCIDevice` dont herite `BLEHCIDevice`)
```python
# mirage/libs/bt.py:405
def isAddressChangeable(bool):
    return self._getManufacturerId() in COMPATIBLE_VENDORS
```

Il est necessaire de verifier que le dongle HCI procuré est compatible avec Mirage. Pour cela il faut trouver la liste des constructeurs compatibles et choisir un dongle parmit eux.
La liste des constructeurs est disponible sur le site officiel de BLuetooth (https://www.bluetooth.com/specifications/assigned-numbers/company-identifiers/)
```python
# mirage/libs/bt_utils/scapy_vendor_specific.py
'''
0: Ericsson Technology Licensing
10: Qualcomm Technologies International, Ltd. (QTIL)
13: Texas Instruments Inc.
15: Broadcom Corporation
18: Zeevo, Inc.
48: ST Microelectronics
57: Integrated System Solution Corp.
'''
COMPATIBLE_VENDORS = [0,10,13,15,18,48,57]
```
Le choix se porte donc sur un CSR8510 de Qualcomm (dongle tres populaire pour ce genre d'outils et utilisé dans GATTAcker) https://www.qualcomm.com/products/csr8510 vendu par Adafruit (https://www.adafruit.com/product/1327)

From https://github.com/securing/gattacker/wiki/FAQ
> The most popular, CSR 8510-based USB dongle is available for about $10, and is confirmed with stable MAC address changing using the Bluez bdaddr tool.

