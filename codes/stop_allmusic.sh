#!/bin/bash


# logフォルダからその音楽の再生時に作成されたログファイルを取得
for LOGPATH in /home/pi/codes/log/*.log
do
    MPG321_PID=`cat ${LOGPATH}`
    rm ${LOGPATH}

    # killコマンドを実行
    kill ${MPG321_PID}
done