#!/bin/bash

if [ -z "$1" ] 
then 
    echo "Usage: run.sh [MainClassName] e.g. MP3_PartA/B/C/D/F"
    exit 1
fi 

mvn package

spark-submit --class $1 target/mp3_sparksql-1.0.0-SNAPSHOT.jar 
