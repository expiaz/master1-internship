```{=latex}
\clearpage
```

# Locate

This module uses the `BCC micro:bit`, make sure it's plugged in your PC.  
Module `ble_locate` at `src/modules/ble_locate.py`, locate nearby BLE devices and sniff connections.  
The localisation is based on the presence of `TxPower` in the advertisement, even if it's possible de sometimes find `TxPower` in the *GATT*, I choose not to connect to the target device if it's missing from the *GAP* because it's supposed to be a stealth attack.

## Parameters

| Parameter | default value | possible value | description |
|-|-|-|-|
| ENVIRONMENT_FACTOR | 2 | 0 to 4 | losses due to environment, 0 is space, 4 is confined |
| INTERFACE | microbit0 | microbitX | micro:bit board to use |
| TIME | 5 | <number> | Scan duration |
| DEVICE_CALLBACK | None | `print` | callback to use for periodic updates during scan |
| CONNECTION_CALLBACK | None | `print` | callback to use for periodic updates during scan |
| WINDOW | 20 | <number> | size of RSSI samples on which sum is calculated to obtain actual RSSI |
| SCAN_TYPE | all | devices, connections | scan realised, micro:bit can only sniff wether devices or connections at a time |

Use mirage CLI entrypoint to issue commands:
```bash
libs/mirage/mirage_launcher ble_locate
```