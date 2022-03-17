#!/bin/bash
originalpath="$(pwd)"
cd "$(cd "`dirname $0`" && pwd)/../" || exit
if [ ! -d "./env/" ]
then
  virtualenv env
  pip3 install -r ./requirements.txt
fi
source "./env/bin/activate"

for f in ./inputFiles/Project1/*.c;
do
#  echo $(sed 's/inputFiles\///1' $(echo $f))
  echo "Processing $f ";
  name=${f##*/}
  python3 ./src/main.py "$f" > ./testFiles/Project1/testOutput/"${name::-2}.txt"
done


cd "$originalpath" || exit