#!/usr/bin/env bash

mkdir -p pgn/eco

for base in A B C D E
do
    for a in $(seq 0 9)
    do
        for b in $(seq 0 9)
        do
            eco="${base}${a}${b}"
            echo "creating pgn/eco/${eco}.pgn"
            for file in pgn/twic[0-9]*.pgn
                do python3 -m search -e "${eco}" -f "${file}" >> "pgn/eco/${eco}.pgn"
            done
        done
    done
done