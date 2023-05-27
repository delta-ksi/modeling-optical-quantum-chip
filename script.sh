#!/bin/bash

data_folder_name='mz_2'

noises=" \
1e-4 \
1e-2"

i=1
for n in $noises
do
    echo "SCRIPT: Launch number $i; Noise is $n."
    ./launch.sh $data_folder_name -n$n
    echo " "
    let i=$i+1
done

python3 ./means.py $(find ./result/$data_folder_name -type f -name "data")