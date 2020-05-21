FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y bluez bluetooth usbutils
RUN apt-get install -y python3 python3-venv python3-pip

WORKDIR /poc
EXPOSE 80

RUN git clone git://redmine.laas.fr/laas/mirage.git
RUN cd mirage && python3 setup.py install

#CMD ["./mirage_launcher", "ble_info"]