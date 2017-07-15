#!/bin/bash

#declare -a robots=('shinbot' 'spherebot' 'snakebot' 'crabbot' '1' '2' '3' '4' 'quadruped' 'starfishbot')
declare -a robots=('1' '2')
for i in ${robots[@]}; do
	python fillDiversityPool.py -r $i -n 300 -t 10
done
