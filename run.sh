#!/bin/bash
source "./env/bin/activate"

#echo "${@:2}"
#echo "${@}"
python3 ./src/main.py "$1" "${@:2}"