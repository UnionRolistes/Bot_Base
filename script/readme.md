# script

## config.sh

il permet de mettre a jour tout les env sans avoir a tripatouiller les fichiers .env

## config_all.sh

il permet de mettre a jour tout les env sans avoir a tripatouiller les fichiers (met aussi a jour les env de toutes les extension).env

## build_all.sh

il construit tout le docker-compose avec la base et toutes les extensions

## start

lance le docker-compose \
(il faut avoir construit le docker-compose avant) \
(les services serotn temporairement inacessible moins de 10s)

## usage

```bash
    # pwd = /xxxxxxxxxxxxx/union_des_rolistes/Bot_Base
    ./config_all.sh
    ./build_all.sh
    ./start.sh
```
## clone bot and plug-in
```bash
cd Bot-Base
./script/config_all.sh 
./script/build_all.sh
./script/start.sh
./update.sh (normalemnt pas besoin)
...
```
## installation et paramétrage de Docker et WSL

pour windows:
installer wsl -> https://learn.microsoft.com/fr-fr/windows/wsl/install 
installer docker -> https://docs.docker.com/engine/install/

pour linux:
installer docker -> https://docs.docker.com/engine/install/ubuntu/
liste des commandes:
1-sudo apt-get install docker.io 
2-sudo systemctl 
3-start docker
4-sudo usermod -aG docker your_username
5-docker version 
6-mkdir dossier
7-cd dossier
8-git clone lien-site_
9-docker-compose -f docker-compose.yml ../Bot_Planning_python/bot/docker-compose.yml config > conf-build-docker-compose.yml