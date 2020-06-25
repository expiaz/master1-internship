FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y bluez bluetooth usbutils
RUN apt-get install -y python3 python3-venv python3-pip
# it can save your life... If you know how to escape from within (esc :wq)
RUN apt-get install -y vim
# server dependencies
RUN pip3 install flask eventlet flask-socketio

EXPOSE 5000

# we won't install mirage
# because we will use mountpoints afterwards
# to be able to edit the code locally
# without having to rebuild the docker image

# mirage dependencies
WORKDIR /poc
COPY libs/mirage-requirements.txt .
RUN pip3 install -r mirage-requirements.txt

#RUN python3 setup.py egg_info
#RUN pip3 install -r mirage.egg-info/requires.txt

RUN rm mirage-requirements.txt

# launch Flask server on localhost:5000
# commented out because devices are unrealiable
# and can crash mirage between attacks
# thus crashing Flask and closing the container
# so it's easier to launch it manually when needed
# and kill it when it crashes, it also gives access to
# the execution trace of the error
#CMD [ "python3", "server/app.py" ]