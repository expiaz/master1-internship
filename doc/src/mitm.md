```{=latex}
\clearpage
```

# Man In The Middle

Available from `ble_mitm` as an integrated Mirage module. As detailed in the documentation^[https://homepages.laas.fr/rcayre/mirage-documentation/blemodules.html#ble-mitm] this module relies heavily on `scenarios`^[https://homepages.laas.fr/rcayre/mirage-documentation/blemodules.html#id113] to achieve on the fly packet modification, otherwise it will display then retransmit the traffic.  
The module needs 2 `hci` devices such as `CSR8510` in order to function properly.

## Parameters

`INTERFACE1` will clone then maintain the connection to the target peripheral, after what `INTERFACE2` will spoof and wait for the central to connect. Once it's connected, the traffic is retransmitted between `INTERFACE1` and `INTERFACE2`.  
By default, Mirage will spoof both the central and the peripheral by setting `INTERFACE1` and `INTERFACE2` to their BD address.  
`ble_mitm` can deal with encryption using `ble_crack`, for more information refer to the documentation^[https://homepages.laas.fr/rcayre/mirage-documentation/blemodules.html#id119].

Use mirage CLI entrypoint to issue commands:
```bash
# spoof XX:XX:XX:XX:XX
libs/mirage/mirage_launcher ble_mitm INTERFACE1=hci0 INTERFACE2=hci1 TARGET=XX:XX:XX:XX:XX
# crack the encryption
libs/mirage/mirage_launcher ble_mitm TARGET=XX:XX:XX:XX:XX MASTER_SPOOFING=yes
```