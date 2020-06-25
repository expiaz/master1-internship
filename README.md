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

## Launching PoC

Dependencies:
- `docker`
- `docker-compose`
- `git`

Requirements:
- 1 sniffer [`BBC Micro:bit`](https://microbit.org/)
- 2 BLE dongles [`CSR8510`](https://www.adafruit.com/product/1327)
- [custom mirage firmware](https://redmine.laas.fr/laas/mirage/btlejack-custom-firmware.git) for `BBC Micro:Bit`

1. Custom firmware  
[Flash the `micro:bit`](https://microbit.org/get-started/user-guide/firmware/) with the custom mirage one using a micro-USB to USB-A cable. Plug the `micro:bit` to a PC and drop the custom mirage firmware into the associated drive, normally named **MICROBIT**. You don't have to press the button next to the micro-USB port for it to work, instead it will corrupt the transfer if you press it. The `micro:bit` will normally unmount and then remount it's associated drive after dropping the custom firmware. There should be a file named `DETAILS.TXT` in the associated drive, open it. The file contains informations concerning the hardware and software components on the card. Find the line `Git SHA` and make sure it's the same as this one: `64359f5c786363065a41ec15c348e3d53568da03`. If the associated drive contains a file `FAIL.TXT`, [unplug and replug the board and retry the above operations](https://support.microbit.org/support/solutions/articles/19000082598-maintenance-mode).

2. Patch source code  
Next, patch the source code of the `Mirage` framework. The submodule is located in `poc/libs/mirage`.  
From there an helper script named `apply_patch` will apply the patch automagically for you.
```bash
$ cd poc/libs
$ ./apply_patch.sh
```

1. Generate requirements (optional)  
Mirage needs python packages in order to work properly, those requirements are stored in a file at `libs/mirage-requirements.txt`. You can re-generate this file using python easily:
```bash
$ cd libs/mirage
$ python3 setup.py egg_info
$ mv mirage.egg-info/requires.txt ../mirage-requirements.txt
$ rm -rf mirage.egg-info
```

4. Launch container  
The PoC is served with `Docker`, a `Dockerfile` and corresponding `docker-compose` is provided.  
Use the bash script `run` to start the container and get a shell into.
```bash
$ cd poc
$ ./run.sh
```
There is also the `stop` shell script which does the reverse (i.e. teardown the container).

Once you are in the container, the files are in `/poc` root folder.
```bash
root@mirage# cd /poc
root@mirage# python3 app.py
```

5. Dashboard  
Then open a web browser to `http://localhost:5000` to get the interface, from there you`ll be able to identify targets and launch live attacks.
```bash
$ chrome http://localhost:5000
```

## Building documentation

Dependencies:
- `pandoc`
- `latex`

```bash
# latex distribution
brew cask install mactex
# pandoc and pandoc filters
brew install pandoc

# build documentation
cd doc
pandoc -d documentation.yaml
open documentation.pdf
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
pandoc -d paper.yaml -o paper.pdf
open paper.pdf
```