#!/bin/bash
sleep 3
container=$(docker ps | grep picture_tagger_server | head -1 | cut -d' ' -f1)
docker logs -f $container
