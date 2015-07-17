#!/bin/sh

#create database persistance container
docker run -v /var/lib/pgsql/data --name dbdata postgres /bin/true

#create postgres database container image
cd setup_docs/DockerPostgresImage
docker build -t mosesdb .
cd ../..

#start postgres database container
docker run -d --volumes-from dbdata --name mosesdb mosesdb

#create serve image
docker build -t mosesweb .
docker run --link mosesdb:localhost -p 8000:8000 -d --name mosesweb mosesweb

echo "All set. Give it a try."
