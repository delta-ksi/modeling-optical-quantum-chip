#!/bin/bash

data_folder_name='CNOT-ODRS/with-phase-nn-noise-1e-2'

noises="\
1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2"

i=1
for n in $noises
do
    echo "SCRIPT: Launch number $i; Noise is $n."
    ./launch.sh $data_folder_name -n$n -c
    echo " "
    let i=$i+1
done

# python3 ./means.py $(find ./result/$data_folder_name -type f -name "data")
