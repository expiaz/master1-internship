
# Outils offensif

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