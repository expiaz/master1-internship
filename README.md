# Projet stage M1 CSSE

*Sujet*: PoC attaques BLE  
*Réalisé par*: Gidon Rémi  
*Date*: 13 Avril - Juin 2020 (10 semaines)  
*Université*: Bretagne Sud  
*Diplôme préparé*: Master 1 Ingénierie de Systèmes Complexes  
*Spécialité*: Cybersécurité des Systèmes Embarqués  

## Retrieve repo
git clone --recursive https://.../ble-internship.git && cd ble-internship

## Building report

Dependencies:
- `pandoc`
- `latex`
- `pandoc-crossref`
- `pandoc-citeproc`

```bash
# latex distribution
brew cask install mactex
# pandoc and pandoc filters
brew install pandoc pandoc-crossref pandoc-citeproc
# build paper
cd rapport
pandoc -d pandoc.yaml -o paper.pdf
open paper.pdf
```

## Building doc
cd doc
sphinx?

## Patching Mirage source code
cd poc/mirage
git apply ../mirage.patch

## Building the image
cd poc
docker-compose up -d
chrome http://localhost:3000