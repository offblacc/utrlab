#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

start_time=$(date +%s.%3N)

for i in {1..14} # broj ispitnih primjera
do
    # generiraj ime direktorija s vodecom nulom
    dir=$(printf "%0*d\n" 2 $i)
    # pokreni program i provjeri izlaz
    res=`python3 MinDka.py < lab2.tests/test$dir/t.ul | diff lab2.tests/test$dir/t.iz -`
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
