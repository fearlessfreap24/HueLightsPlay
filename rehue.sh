#! /bin/sh

docker stop hue
docker rm hue
docker build -t huelights ./
docker run -d -p 5000:5000 -v $JJDB:/mnt/db --name hue huelights 