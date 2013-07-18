#!/bin/bash

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

rm file_list.txt

for FILE in `ls *.mp4`
do
    echo $FILE >> file_list.txt
done

IFS=$SAVEIFS
