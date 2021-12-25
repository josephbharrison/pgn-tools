#!/usr/bin/env bash

files=$1
[[ -z $files ]] && files=pgn/twic/twic[0-9]*.pgn

mkdir -p pgn/eco

for base in A B C D E
do
    for a in $(seq 0 9)
    do
        for b in $(seq 0 9)
        do
            eco="${base}${a}${b}"
            echo "creating pgn/eco/${eco}.pgn"
            for file in $files
                do python3 -m search -e "${eco}" -f "${file}" >> "pgn/eco/${eco}.pgn"
            done
        done
    done
done
