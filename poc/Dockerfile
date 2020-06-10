FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y bluez bluetooth usbutils
RUN apt-get install -y python3 python3-venv python3-pip
RUN apt-get install -y vim

EXPOSE 5000

# dev
# we won't install mirage
# because we will use mountpoints afterwards
# to be able to edit the code locally
# without having to rebuild the docker image

RUN mkdir /poc && cd /poc
COPY libs/mirage /poc/mirage

RUN cd /poc/mirage && \
    python3 setup.py egg_info && \
    pip3 install -r mirage.egg-info/requires.txt

RUN pip3 install flask

RUN rm -rf /poc && mkdir /poc

