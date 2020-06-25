```{=latex}
\clearpage
```

# Conclusion

Les mécanismes du `BLE` évoluent pour rester viable dans son marché d'objets intelligents facilitant l'interaction homme-machine. Il dispose des mécanismes nécessaires pour mettre en place un niveau de sécurité acceptable pour les standards contemporains. La recherche d'interoperabilité engendre encore des vulnérabilités, mais avec la prochain dépréciation du protocole 4.0, et donc des connexions *legacy*, l'écoute passive ne devrait plus être une menace car la version 4.2 met en place les connexion sécurisées basées sur *Diffie-Hellman*. La plupart des vulnérabilités restantes seront de l'ordre utilisateur plutôt que d'un défaut de conception du protocole. Il n'empêche que la majorité des constructeurs n'utilisent toujours pas les mécanismes fournis par le `BLE` mais leur solution personnalisée.

Le projet s'est plus rapproché d'une étude de recherche et développement plutot que d'un projet de stage que j'ai eu l'occasion de retrouvé en entreprise par le passé. Le sujet à demandé un effort de documentation et de compréhension (etude du protocole BLE, des attaques existantes, du materiel et des outils disponibles pour l'analyser) plus important que le développement (*front* & *back-end* puis intégration du framework `Mirage` avec ajout d'un nouveau module).  
Ce n'est cependant pas pour me déplaire puisque j'éprouve un certain intérêt pour la compréhension et l'étude des systèmes dans les moindres détails, je suis également toujours plus à l'aise en travaillant sur un système compris et maîtrisé, ce qui me permet de voir l'étendue des possibilités, plutôt que de me jeter directement dans le développement.

Ce projet m'a permit de me plonger totalement dans le réseau, d'en analyser la structure/couches et jouer avec les outils de dissection (`wireshark`, `scapy`), comblant un certain manque dans les années d'étude précédentes.  
Le seul bémol reste les conditions exceptionnelles dans lequel il a été réalisé obligeant de travailler avec une connexion factice plutôt que des appareils commercialisés, ce qui aurait permit une consolidation des observations avancées.

```{=latex}
\clearpage
```