# Projet stage M1 CSSE

*Sujet*: PoC attaques BLE  
*Réalisé par*: Gidon Rémi  
*Date*: 13 Avril - Juin 2020 (10 semaines)  
*Université*: Bretagne Sud  
*Diplôme préparé*: Master 1 Ingénierie de Systèmes Complexes  
*Spécialité*: Cybersécurité des Systèmes Embarqués  

## Clone repository

```bash
$ git clone --recursive https://gitlab.com/hackrf/hackrf-domotique.git
$ cd hackrf-domotique
```

## Files architecture



## Launching PoC

Dependencies:
- `docker`
- `docker-compose`
- `git`

First you need to patch the source code of one of the modules: `Mirage`. The submodule is localted in `poc/libs/mirage`.  
From there an helper script named `apply_patch` will apply the patch automagically for you.
```bash
$ cd poc/libs
$ ./apply_patch.sh
```

The PoC is served with `Docker`, a `Dockerfile` and corresponding `docker-compose` is provided.  
Use the bash script `run` to start the container and get a shell into.
```bash
$ cd poc
$ ./run.sh
```
There is also the `stop` shell script which does the reverse (i.e. teardown the container).

Once you are in the container, the files are in `/poc` root folder.
```bash
root@mirage# cd /poc/server
root@mirage# python3 app.py
```

Then open a web browser to `http:localhost:8080` to get the interface, from there you`ll be able to identify targets and launch live attacks.
```bash
$ chrome http://localhost:8080
```

## Building paper

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
cd paper
pandoc -d pandoc.yaml -o paper.pdf
open paper.pdf
```