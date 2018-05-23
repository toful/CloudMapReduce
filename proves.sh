#!/bin/bash

#This script will run automatically 3 server, a registry for this servers and a client in three diferent gnome-terminals with different combinatios of
# wc/cw, number of mappers, and files
#filename="Sherlock_x50.txt Sherlock_x100.txt"

filename="Sherlock.txt Sherlock_x5.txt Sherlock_x10.txt Sherlock_x50.txt Sherlock_x100.txt"
nummappers="1 2 4 8 16 32 64"
operation="WC CW"

for k in $operation;
do
	for i in $filename;
	do
		for j in $nummappers;
		do
			echo $i $j $k
			python run.py $i $j $k
		done
	done
done
exit 0
