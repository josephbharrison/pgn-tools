#!/usr/bin/env bash

mkdir -p pgn/twic
cd pgn/twic || exit 1

twic_min=$1
twic_max=$2

[[ -z $twic_min ]] && twic_min=920
[[ -z $twic_max ]] && twic_max=1414

# download all pgn files
for file in $(seq $twic_min $twic_max)
do
    wget "https://theweekinchess.com/zips/twic${file}g.zip"
done

# unzip pgn
for file in *.zip
do
    [[ -e "$file" ]] || break
    unzip -o "$file"
    rm "$file"
done

# concatenate all pgn files
[[ -f twic.pgn ]] && rm twic.pgn
for file in *.pgn
do
    [[ -e "$file" ]] || break
    cat "${file}" >> twic.pgn
    echo "" >> twic.pgn
done
