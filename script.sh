#!/bin/bash

data_folder_name='chip2x2/with-phase'

noises="\
1e-5 1e-5 1e-5 1e-5 1e-5 1e-5 1e-5 1e-5 1e-5 1e-5 \
1e-5 1e-5 1e-5 1e-5 1e-5 1e-5 1e-5 1e-5 1e-5 1e-5"

i=1
for n in $noises
do
    echo "SCRIPT: Launch number $i; Noise is $n."
    ./launch.sh $data_folder_name -n$n -c
    echo " "
    let i=$i+1
done

# python3 ./means.py $(find ./result/$data_folder_name -type f -name "data")
