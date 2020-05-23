# Bluetooth Low energy

multi bande
master - slave
packet based

## Stack

## Finding
advertisements

adv packet structure
GAP AD type
https://www.silabs.com/community/wireless/bluetooth/knowledge-base.entry.html/2017/02/10/bluetooth_advertisin-hGsf
https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile/

## pairing

phase 1
feature exchange
https://www.bluetooth.com/blog/bluetooth-pairing-part-1-pairing-feature-exchange/

phase 2
key generation method

### JustWorks
https://www.bluetooth.com/blog/bluetooth-pairing-part-2-key-generation-methods/?utm_campaign=developer&utm_source=internal&utm_medium=blog&utm_content=bluetooth-pairing-part-1-pairing-feature-exchange

phase 3
temp key generation and short/long term key derivation


## Communication

GATT & ATT proto
https://fr.mathworks.com/help/comm/examples/modeling-of-ble-devices-with-heart-rate-profile.html

interop via profiles (API commune) -> GATT protocole

All Bluetooth Low Energy devices use the Generic Attribute Profile (GATT). The application programming interface offered by a Bluetooth Low Energy aware operating system will typically be based around GATT concepts.[44] GATT has the following terminology:

Client
A device that initiates GATT commands and requests, and accepts responses, for example, a computer or smartphone.
Server
A device that receives GATT commands and requests, and returns responses, for example, a temperature sensor.
Characteristic
A data value transferred between client and server, for example, the current battery voltage.
Service
A collection of related characteristics, which operate together to perform a particular function. For instance, the Health Thermometer service includes characteristics for a temperature measurement value, and a time interval between measurements.
Descriptor
A descriptor provides additional information about a characteristic. For instance, a temperature value characteristic may have an indication of its units (e.g. Celsius), and the maximum and minimum values which the sensor can measure. Descriptors are optional – each characteristic can have any number of descriptors.

fonctionnement apparaige (phases)

## BLE

specification du Bt pour les systemes embarques, bcp utilise dans objets connectes

4.0 arrivee

4.2 securite

5.0 mesh networks for home automation or sensor networks
use bluetooth mesh profile General Access Profile (GAP)

5.1 localisation

Utilisation "abusive" dans les objets connectes ?

### Flaws

#### Downgrade

“SC”
The SC field is a 1-bit flag that is set to one to request LE Secure Connection pairing. The possible resulting pairing mechanisms are if both devices support LE Secure Connections, use LE Secure Connections and otherwise use LE legacy pairing. So this flag is an indicator to determine Phase 2 pairing method.

