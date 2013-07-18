#!/bin/bash

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

for FILE in `ls *.flv`
do
    echo $FILE
    ffmpeg -i "$FILE" -ar 22050 "${FILE%.flv}.ogv" 
    # ffmpeg -i "$FILE" -vcodec libx264 "${FILE%.flv}.mp4" 
    rm $FILE
done

for FILE in `ls *.mp4`
do
    echo $FILE
    ffmpeg -i "$FILE" -ar 22050 "${FILE%.flv}.ogv" 
    # ffmpeg -i "$FILE" -vcodec libx264 "${FILE%.flv}.mp4" 
    rm $FILE
done

IFS=$SAVEIFS
