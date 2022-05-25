#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

set -e
gcc parser.c -o parser.out
set +e

start_time=$(date +%s.%3N)

for i in {1..20} # broj ispitnih primjera
do
    # generiraj ime direktorija s vodecom nulom
    dir=$(printf "%0*d\n" 2 $i)
    # pokreni program i provjeri izlaz
    res=`./parser.out < lab4.tests/test$dir/test.in | diff lab4.tests/test$dir/test.out -`
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

end_time=$(date +%s.%3N)
elapsed=$(echo "scale=3; $end_time - $start_time" | bc)
echo "elapsed time: $elapsed s"