```{=latex}
\clearpage
```

# Dashboard

The interface is quite simple, it consists of controls to start/stop scans at the top left, a map of located devices, logs from Mirage execution in back-end and last but no least the list of found devices as well as connections. Each row contain informations who can later be used to launch attacks from the CLI using Mirage.  

The map scales to the farthest device found, other distances are scaled relatively to it.  
In the picture below we can see the map is using the blue circle having a radius of 5.62 meters as it's scale. The nearest device, yellow one, only at 79 cm is much smaller and close to our point, which is the centered black spot.

![Map of located devices](img/radar.png){width=50%}