#!/bin/sh

rm *.wma

mp3wrap ${1}_tmp.mp3 *.mp3
mv ${1}_tmp_MP3WRAP.mp3 ${1}_tmp.mp3
mid3v2 -D ${1}_tmp.mp3
mid3v2 -t ${1}  ${1}_tmp.mp3
ffmpeg -i ${1}_tmp.mp3 -acodec libmp3lame -ab 192k ${1}.mp3
rm ${1}_tmp.mp3
mv ${1}.mp3 ../output/
rm -f *.mp3
