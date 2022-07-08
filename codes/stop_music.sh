#!/bin/bash

# mp3ファイル名が指定されているかチェックする
if [ $# != 1 ]; then
    echo "usage: ./stop_music.sh 'hoge.mp3'"
    exit 1
fi

# logフォルダからその音楽の再生時に作成されたログファイルを取得
MUSICFILE=`basename $1`
LOGPATH=/home/pi/codes/log/${MUSICFILE}.log
MPG321_PID=`cat ${LOGPATH}`
rm ${LOGPATH}

# killコマンドを実行
kill ${MPG321_PID}