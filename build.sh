#!/bin/bash

# if an env directory is not present
if [ ! -d "./env/" ]
then
#  make one
  virtualenv env
#  install the necessary packages
  pip3 install -r ./requirements.txt
fi
sudo java -jar antlr.jar -Dlanguage=Python3 ./src/g4_files/CGrammar.g4 -visitor