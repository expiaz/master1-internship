---
nocite: |
  @*
...

Due aux conditions exceptionnelles imposées par la pandémie du COVID-19, j'ai réalisé un sujet fourni par le laboratoire d'informatique LAB-STICC affilié à l'université dans le cadre du stage de première année de master CSSE à l'UBS de Lorient.  
Initialement prévu sur l'étude les protocoles de communication domotique (`ZigBee`, `Z-Wave`, `Thread` ...) à l'aide d'une carte `HackRF`, j'ai dû m'adapter avec le confinement et ait bifurqué sur du matériel et un protocle accessible: le *Bluetooth Low Energy*. Son intégration dans nombre d'appareils de bureautique en ont fait un choix pour la communication avec les systèmes embarqués constituant les objets intelligents. L'étude du protocole est facilitée par cette popularité, disposant de matériel dédié à moindre coût sur le marché ainsi qu'une floppée d'outils logiciels et d'audits de sécurité révélant et expliquant les vulnérabilités du protocole.

Dans le cadre du master CSSE nous étudions l'internet des objets (*IoT*) et leurs aspects sécurité. Le protocole réseau sans fil *Bluetooth Low Energy* (`BLE`) permet une consommation réduite pour les objets fonctionnant sur batterie, visant notamment les objets connectés. Aujourd'hui integré dans la plupart des appareils de bureautique, il est rapidement devenu populaire dans l'internet des objets.

La première itération du BLE ne répond plus aux exigences de sécurité contemporaine et même si le protocole à su évoluer depuis pour répondre à ces besoins, beaucoup d'appareils utilisent encore la version originale n'intégrant pas ces mécanismes.  
Ce sont pour la plupart des appareils conçus pour fonctionner sur batterie et communiquer en point à point. On va retrouver les capteurs corporels pour santé ou fitness mais également des mécanismes plus sensibles tels des cadenas ou serrures. Les communications (incluant parfois des données personnelles) peuvent êtres interceptées, voir modifiées pour permettre des actions aux dépends de l'utilisateur.