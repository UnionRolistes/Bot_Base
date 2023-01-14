# find all docker-compose.yml files with depth 3 add '-f' to each file stored in COMPOSE_FILES var
COMPOSE_FILES=`find ../ -maxdepth 3 -name docker-compose.yml -exec echo -f {} \;`
# echo $COMPOSE_FILES
docker-compose $COMPOSE_FILES config > compose-build.yml