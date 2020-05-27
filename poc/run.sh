#!/bin/bash

#docker run -ti --privileged --name=mirage --net=host poc/mirage /bin/bash

# build and start the container in the background
docker-compose -f docker-compose.yml up -d
# get a shell into the container
docker exec -it mirage /bin/bash