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
