```{=latex}
\clearpage
```

# Tests

The project provide a test network mocking a slave and BLE master based on Mirage `ble_slave` and `ble_master` modules. Those modules are customised using scenarios `MockMaster` and `MockSlave` found in `poc/src/scenarios`. The scenarios add CLI parameters to modify their behaviors besides those used by their modules.

## MockSlave

| Parameter | default value | possible value | description |
|-|-|-|-|
| INTERFACE | hci0 | hciX | hci device to use |
| SCENARIO | MockSlave | <scenario> | scenario to use |
| NAME | Test Slave | <string> | local name emitted in the advertisement |
| PAIRING | yes | <boolean> | enable pairing |
| TXPOWER | -55 | <integer> | signal strength measured 1 meter away from device |

## MockMaster

| Parameter | default value | possible value | description |
|-|-|-|-|
| INTERFACE | hci1 | hciX | hci device to use |
| SCENARIO | MockMaster | <scenario> | scenario to use |
| NAME | Test Slave | <string> | local name used to iddentify target slave |
| PAIRING | yes | <boolean> | enable pairing |
| TARGET | scan for slave | BD address | slave BD address, scan devices if empty |
| REQUESTS | 10 | <integer> | number of requests issued to slave device during the connection |
| INTERVAL | 3 | <number> | time in seconds between each request to slave |

Use mirage CLI entrypoint to issue commands:
```bash
# start slave
libs/mirage/mirage_launcher ble_slave
# start master
libs/mirage/mirage_launcher ble_master
```
Use `--debug` switch to activate debug mode and see exception traces.  
Be aware that mirage will stay in foreground while executing thus blocking the CLI until it finishes, use `&` parameter to start a task in background, even if it's recommended to start each mirage task in it's own shell for output readability.