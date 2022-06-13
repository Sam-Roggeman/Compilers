#!/bin/bash
for file in ./inputFiles/CompilersBenchmark/CorrectCode/*.c
do
  source ./run.sh "$file" "${@}"
done