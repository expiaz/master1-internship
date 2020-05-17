FROM Ubuntu:18.04

RUN apt update && \
    apt install -y python3 python3-venv python3-pip

WORKDIR /poc/mirage
#EXPOSE 80

# Use the previously downloaded mirage git repo for install only
COPY mirage .
RUN python3 setup.py install

# we will use mountpoints from now on
RUN rm -rf mirage/scenarios