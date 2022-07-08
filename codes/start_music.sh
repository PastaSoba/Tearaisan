#!/bin/bash

# mp3ファイルが指定されているかチェック
if [ $# != 1 ]; then
    echo "usage: ./start_music.sh 'hoge.mp3'"
    exit 1
fi

# 既に同名のmp3ファイルが再生されている時に備え、
# 同名のmp3ファイルの再生を停止する
/home/pi/codes/stop_music.sh $1

# mp3ファイルを再生
mpg321 $1 &> /dev/null &

# 流している音楽のmpg321のプロセスIDをログに保存
# 音楽を停止するときに用いる
MUSICFILE=`basename $1`
LOGPATH=/home/pi/codes/log/${MUSICFILE}.log
echo $! > ${LOGPATH}
