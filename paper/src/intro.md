Due aux conditions exceptionnelles imposees par la pandemie du COVID-19, j'ai réaliser un sujet fournie par le laboratoire d'informatique LAB-STICC, affilié a l'université dans le cadre du stage de premiere annee de master CSSE a l'UBS de Lorient.  
Je devais d'abors travailler avec une carte HackRF pour etudier les protocoles de communication domotique (ZigBee, ZWave, Thread ...) mais due au confinement j'ai du m'adapter et me suis rabattu sur du materiel et un protocle accessible: le Bluetooth Low Energy. Sont integration dans nombre d'appareils de bureautique en ont fait un choix pour la communication avec les systemes embarques constituant les objets intelligents. l'etude du protocole est facilité par cette popularite, disposant de materiel dedie a moindre cout sur le marché ainsi ainsi qu'une floppée d'outils logiciels et d'audits de securite revelant et expliquant les vulnerabilites du protocole.

Dans le cadre du master CSSE nous étudions l'internet des objets (*IoT*) et leurs aspects sécurité. Le protocole réseau sans fil Bluetooth Low Energy (BLE) permet une consommation réduite pour les objets fonctionnant sur batterie, visant notamment les objets connectés. Aujourd'hui integré dans la plupart des appareils de bureautique, il est rapidement devenu populaire dans l'internet des objets.

La première itération du BLE ne répond plus aux exigences de sécurité contemporaine et même si le protocole à su évoluer depuis pour répondre à ces besoins, beaucoup d'appareils utilisent encore la version originale n'intégrant pas ces mécanismes.  
Ce sont pour la plupart des appareils conçus pour fonctionner sur batterie et communiquer en point à point. On va retrouver les capteurs corporels pour santé ou fitness mais également des mécanismes plus sensibles tels des cadenas ou serrures. Les communications (incluant parfois des données personnelles) peuvent êtres interceptées, voir modifiées pour permettre des actions aux dépends de l'utilisateur.