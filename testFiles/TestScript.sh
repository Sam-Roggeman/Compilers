#!/bin/bash
# cd to the root of the project

cd "$(cd "$(dirname "$0")" && pwd)/../" || exit
#source ./build.sh ../
# if an env directory is not present
if [ ! -d "./env/" ]
then
#  make one
  virtualenv env
  #activate the env
  source "./env/bin/activate"
#  install the necessary packages
  pip3 install -r ./requirements.txt
#  generate the grammar
  sudo java -jar antlr.jar -Dlanguage=Python3 ./src/g4_files/CGrammar.g4
else
  #activate the env
  source "./env/bin/activate"
fi
# loop over all of the projects
for projectnr in 0 1 2
do
# project= name of the project directory
  project="Project${projectnr}"
# if the directory for the output of the tests does not exist
  if [ ! -d "./testFiles/${project}/testOutput/" ]
  then
#    make it
    mkdir "./testFiles/${project}/testOutput/"
  fi
# if there is already a Results.txt
  if [ -f "./testFiles/${project}/Result.txt" ]
  then
#    delete it
    rm "./testFiles/${project}/Result.txt"
  fi
#  if there is already an error.txt
  if [ -f "./testFiles/${project}/comparisonErrors.txt" ]
  then
#    delete it
    rm "./testFiles/${project}/comparisonErrors.txt"
  fi
#  add some explanation to the Results.txt
  echo "# Comparison of the expected output and the actual output" >> "./testFiles/${project}/Result.txt"
  echo "# Filename Success: True = identical outputs" >> "./testFiles/${project}/Result.txt"
#  loop over all the c files
  for f in ./inputFiles/${project}/*.c;
  do
#    extract the name from the path
    name=${f##*/};
    name=${name::-2}
#    execute the compiler and save the output (stderr and stdout) to the testoutput
    python3 ./src/main.py "$f" &> ./testFiles/${project}/testOutput/"${name}.txt";
#    compare the output of the test with the expected output, split the output and potential errors
    python3 ./src/CompareTests.py "./testFiles/${project}/expectedOutput/${name}.txt" "./testFiles/${project}/testOutput/${name}.txt" 1> ./temp1.txt 2>./temp2.txt

    success=$(cat temp1.txt)
    error=$(cat temp2.txt)
    output="${name} Success: ${success}"
    error="${name}: error: ${error}"
#    place the success(True or False) inside of the Results
    echo "${output}" >> "./testFiles/${project}/Result.txt"
#     place the potential errors inside of the errors txt
    echo "${error}" >> "./testFiles/${project}/comparisonErrors.txt"
#   remove the temp files
    rm ./temp1.txt
    rm ./temp2.txt
    RED='\033[0;31m'
    ORANGE='\033[0;33m'
    NC='\033[0m' # No Color
#    if test passed
    if [ "${success}" = "True" ]; then
        echo "${name} has PASSED the test."
    else
#      elif not passed
      if [ "${success}" = "False" ]; then

        echo -e "${RED}${name} has NOT PASSED the test.${NC}"
      else
#        else
        echo -e "${ORANGE}An error has occured comparing expected and actual output of ${name}, check comparisonErrors.txt for more information.${NC}"
      fi
    fi
  done
done

