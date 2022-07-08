import time
import threading
import os
import sys
from enum import Enum
import subprocess

from musicplayer import MusicPlayer
from handwashtimer import HandwashTimer
from distancesensor import DistanceSensor, DistanceSensorManager, DistanceSensorState
from historyediter import HistoryEditer


class TearaiState(Enum):
    STANDBY = 1        # 起動直後/手洗い待機
    DURING = 2         # 手洗い中


class Main:
    def __init__(self, threshold_dist: float, tearaiTime):
        """
        argument:
            threshold_dist: 人が接近したと判断する距離（cm）
        """
        #############
        # 変数の宣言  #
        #############
        self.tearaiState = TearaiState.STANDBY

        ###################
        # インスタンスの作成 #
        ###################
        # 音楽プレイヤー,手洗い用タイマー、距離センサの作成
        self.musicPlayer = MusicPlayer()
        self.handwashTimer = HandwashTimer(tearaiTime)
        distanceSensor = DistanceSensor()
        # 距離の測定開始
        self.distanceSensorManager = DistanceSensorManager(threshold_dist)
        self.distanceSensorManager.addObserver(self)
        self.distanceSensorManager.addSensor(distanceSensor)
        self.distanceSensorManager.startMeasure()


        #####################
        # ファイルへの書き出し #
        ####################
        # プロセスのPIDをファイルに書き出す
        system_pid_log = open("/home/pi/system_pid.log", "w", encoding="utf-8")
        system_pid_log.write(str(os.getpid()))
        system_pid_log.close()

        # 手洗い記録を初期化してファイルに書き出す
        hist = HistoryEditer.loadjson()
        hist["success"] = 0
        hist["failure"] = 0
        HistoryEditer.recordjson(hist)


    def eventListener(self, diststate: DistanceSensorState):
        if self.tearaiState == TearaiState.STANDBY and diststate == DistanceSensorState.HUMAN_IS_NEAR:
            """ 手洗い開始時の処理
            ※「手洗い待機中」かつ「人が近くに来た」とき、手洗いが開始されたと判定
            """
            self.tearaiState = TearaiState.DURING
            self.handwashTimer.startTearai()
            self.musicPlayer.stopall()
            self.musicPlayer.play("/home/pi/Music/harugakita.mp3")
        elif self.tearaiState == TearaiState.DURING and diststate == DistanceSensorState.HUMAN_IS_FAR:
            # 「手洗い中」かつ「人が近くにいなくなった」とき、手洗いが終了したと判定
            self.tearaiState = TearaiState.STANDBY
            result = self.handwashTimer.endTearai()
            if result is True:
                """ 手洗い終了 → 手洗い成功時の処理
                """
                self.musicPlayer.stopall()
                self.musicPlayer.play("/home/pi/Music/seikou.mp3")
                # giveCandy()
                cmd = ["python3", "/home/pi/codes/give_candy.py"]
                subprocess.call(cmd)

                # 手洗い成功を記録する
                hist = HistoryEditer.loadjson()
                hist["success"] = hist["success"] + 1
                HistoryEditer.recordjson(hist)
            else:
                """ 手洗い終了 → 手洗い失敗時の処理
                """
                self.musicPlayer.stopall()
                self.musicPlayer.play("/home/pi/Music/sippai.mp3")

                # 手洗い失敗を記録する
                hist = HistoryEditer.loadjson()
                hist["failure"] = hist["failure"] + 1
                HistoryEditer.recordjson(hist)


if __name__ == "__main__":
    threshold_dist = float(sys.argv[1])
    m=Main(threshold_dist=threshold_dist, tearaiTime=22)

    #####################################################
    # killコマンドが実行されるまで、プログラムを終了させない処理 #
    #####################################################
    # 全てのスレッドの実行が完了するまで、プログラムを終了させないようにする
    # 実際には距離測定スレッドが永久に距離を取得し続けるため、
    # killコマンドが発行されるまでプログラムを終了させないようにすることを意図した
    thread_list = threading.enumerate()
    thread_list.remove(threading.main_thread())
    for thread in thread_list:
        thread.join()
