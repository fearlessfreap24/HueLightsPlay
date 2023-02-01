#! /bin/bash

x=1
while [ $x -ge 1 ]
    do
        echo "Test $x"
        x=$(($x + 1))
        sleep 60
    done