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