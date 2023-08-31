#!/bin/bash
cd ..
#all docker-compose depth 3
tmp=""
find . -maxdepth 3 -name "docker-compose.yml" |while read i; do
    tmp=$tmp + " -f " + $i
done
cd Bot_Base
docker-compose $tmp config > conf-build-docker-compose.yml
#docker-desktop force restart of all containers of the stack
docker-compose -f conf-build-docker-compose.yml up -d --remove-orphans --force-recreate --build
