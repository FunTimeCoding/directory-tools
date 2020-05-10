#!/bin/sh -e

mkdir -p tmp

GROUP=$(id -g -n "${USER}")

sudo slapcat -n 0 -l tmp/configuration.ldif
sudo chmod 600 tmp/configuration.ldif
sudo chown "${USER}:${GROUP}" tmp/configuration.ldif

sudo slapcat -n 1 -l tmp/data.ldif
sudo chmod 600 tmp/data.ldif
sudo chown "${USER}:${GROUP}" tmp/data.ldif
