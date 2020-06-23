```{=latex}
\clearpage
```

# Hijack

As explained in the corresponding documentation^[https://homepages.laas.fr/rcayre/mirage-documentation/blemodules.html#id87], this integrated Mirage module named `ble_hijack` allows to:

> *sniff an established connection, synchronize to it and jam the packet emitted by the slave. As a consequence, if the master reachs its timeout value, it disconnects from the slave device and the attacker is able to communicate with the slave device instead of him.*.

Also, the module is based on `ble_sniff` to identify target connection and only hijacks the connection, as stated in the documentation:

> *this module needs ble_sniff, and cannot be used alone. Indeed, when the connection is hijacked, the module terminates its execution, allowing to run another module, such as ble_master or ble_discover.*

The module can wait for new connections to be created in order to sniff connection parameters required to follow the connection (sniffing mode new connections^[https://homepages.laas.fr/rcayre/mirage-documentation/blemodules.html#hijacking-a-new-connection]) or try to synchronize with an existing connection by recovering connection parameters over time (sniffing mode existing connections^[https://homepages.laas.fr/rcayre/mirage-documentation/blemodules.html#hijacking-an-existing-connection]).  

## Parameters

An interesting parameter is that you can provied a `pcap` file to capture the attack and analyze it later using *Wireshark*. In order to be able to capture the traffic pass `PCAP_FILE=/path/to/file.pcap` where `/path/to/file.pcap` is an absolute path to a non-existent file.  
For all possible parameters, refer to the module documentation^[https://homepages.laas.fr/rcayre/mirage-documentation/blemodules.html#id95].

Use mirage CLI entrypoint to issue commands:
```bash
# Hijack then capture connection with a shell as master
libs/mirage/mirage_launcher "ble_hijack|ble_master" HIJACKING_MODE=existingConnections
# equivalent to launching ble_hijack directly
libs/mirage/mirage_launcher "ble_sniff|ble_master" INTERFACE=microbit0 SNIFFING_MODE=existingConnections HIJACKING=yes
```

## Troubleshooting

can take time to catch up connection bc bbc jumps but also conn, possible para not integrated in mirage to monitor multiple data chan