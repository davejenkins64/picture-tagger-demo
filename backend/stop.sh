#!/bin/bash

container=$(docker ps | grep picture_tagger_server | head -1 | cut -d' ' -f1)
if [ -n "$container" ]
then
    echo "Killing existing container $container"
    docker kill $container
fi
