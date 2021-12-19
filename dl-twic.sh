#!/usr/bin/env bash

mkdir pgn
cd pgn

# download all pgn files
for file in $(seq 920 1415)
do
    wget https://theweekinchess.com/zips/twic${file}g.zip
done

# unzip pgn
for file in $(ls -1 *.zip);
do
    unzip $file
done

# concatenate all pgn files
forfile in $(ls -1 *.pgn)
do
    cat ${file} >> twic.pgn
    echo "" >> twic.pgn
done
