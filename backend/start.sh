#!/bin/bash

if [ -z "$BACKEND_IP" ]
then
	echo "FATAL: set BACKEND_IP to the server's ip address first"
	exit 1
fi

# Assume Apache/Nginx is running on the same server as backend
if [ -z "$WEBSERVER_PICTURE_ROOT" ]
then
	echo "FATAL: set WEBSERVER_PICTURE_ROOT to the web server's docroot for pictures"
    echo "and make sure it ends with a /"
	exit 1
fi

docker run -d \
    -p $BACKEND_IP:5000:5000 \
    -e WEBSERVER_PICTURE_ROOT=$WEBSERVER_PICTURE_ROOT \
    --mount type=bind,source="${PWD}"/data,target=/usr/src/api/data \
    picture_tagger_server
