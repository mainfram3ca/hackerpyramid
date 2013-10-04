#!/bin/bash

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

for FILE in `ls *.flv`
do
    echo $FILE
    avconv -i "$FILE" -c:v libx264 "${FILE%.flv}.mp4" 
    rm $FILE
done

IFS=$SAVEIFS
