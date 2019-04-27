#!/bin/bash
#########################################
# author : Team Elfs
# script : bash script for build and install of cmpe-272
#########################################

DCRFLASK=elfs-project-flask
DCRNGNX=elfs-project-nginx
DCRNET=elfs-project-network
DCRMONGODB=elfs-project-mongodb
DCRNGNXNAME=nginx
DCRFLASKNAME=project-flask
DCRMONGODBNAME=project-mongodb
MONGODBPERSIST=/var/www/project-mongodb

function create_mongo_db_dir() {
    if [ ! -d $MONGODBPERSIST ]; then
        echo "creating persistent mongodb directory"
        mkdir -p $MONGODBPERSIST
    fi
}

function build_elfs_project_app() {
    echo "Building ...."
	docker build -t $DCRFLASK -f Dockerfile-project-flask .
	docker build -t $DCRNGNX -f Dockerfile-project-nginx .
	docker build -t $DCRMONGODB -f Dockerfile-project-mongodb .
}

function deploy_elfs_project_app() {
    echo "Deploying Team Elf's webserver and application..."

    #create_mongo_db_dir
	docker network create $DCRNET
	docker run -d --name $DCRFLASKNAME --net $DCRNET -v "./project-app" $DCRFLASK
	docker run -d --name $DCRNGNXNAME --net $DCRNET -p "80:80" $DCRNGNX
	docker run -d --name $DCRMONGODBNAME -d -v $MONGODBPERSIST:/data/db -p 27017:27017 $DCRMONGODB
    docker ps

}

function clean_elfs_project_app() {
    echo "Cleaning Team Elfs webserve and applicatio..."
    docker kill $DCRFLASKNAME $DCRNGNXNAME $DCRMONGODBNAME
    docker rm $DCRFLASKNAME $DCRNGNXNAME $DCRMONGODBNAME
    docker network rm $DCRNET
    docker rmi $DCRNGNX $DCRFLASK $DCRMONGODB
}

function stop_elfs_project_app() {
    echo "Stopping Team Elfs webserve and applicatio..."
    docker kill $DCRFLASKNAME $DCRNGNXNAME $DCRMONGODBNAME
    docker rm $DCRFLASKNAME $DCRNGNXNAME $DCRMONGODBNAME
    docker network rm $DCRNET
    docker ps
}

# Usage info
usage() {
cat << EOF
Usage: ${0##*/} [-b] [-c] [-i] [-h]
This script is for build and deploy webserver and application

    -b          build the containers needed for deployment
    -c          clean the containers, (stop and clean the container images)
    -i          start the containers  webserver, uwsgi, app server and mongodb
    -s          stop the running containers
    -h          help
EOF
    exit 1;
}

function main() {

    if [[ $# -eq 0 ]] ; then
        usage
        exit 0
    fi

    while getopts "bcihs" o; do
        case "${o}" in
        b)
            build_elfs_project_app
            ;;
        c)
            clean_elfs_project_app
            ;;
        i)
            deploy_elfs_project_app
            ;;
        s)
            stop_elfs_project_app
            ;;
        h)
            usage
            ;;
        *)
            usage
            ;;
        esac
    done
    shift 0

}

main $@
