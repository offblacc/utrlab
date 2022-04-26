#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

for i in {1..25} # broj ispitnih primjera
do
    # generiraj ime direktorija s vodecom nulom
    dir=$(printf "%0*d\n" 2 $i)
    # pokreni program i provjeri izlaz
    res=`python3 SimPa.py < lab3.tests/test$dir/primjer.in | diff lab3.tests/test$dir/primjer.out -`
    if [ "$res" != "" ]
    then
        # izlazi ne odgovaraju
        echo "Test $dir ${red}FAIL${reset}"
        echo $res
    else
        # OK!
        echo "Test $dir ${green}PASS${reset}"
    fi
done
