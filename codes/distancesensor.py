import threading
import time
import RPi.GPIO as GPIO
from enum import Enum
import queue


class DistanceSensorState(Enum):
    STANDBY = 1        # 起動直後
    HUMAN_IS_NEAR = 2  # 人が近くにいる
    HUMAN_IS_FAR = 3   # 人が近くにいない


class DistanceSensorManager:
    """距離センサの生成、Mainクラスへの距離変化イベント通知を行う
    method:
        addObserver:
            通知の送り先のオブジェクトを登録する
        notifyObserver
            登録されたオブジェクトに通知を送る
    """
    def __init__(self, threshold_dist):
        self.threshold_dist = threshold_dist
        self.diststate = DistanceSensorState.STANDBY
        self.observer = None
        self.sensor   = None

    def addObserver(self, observer: "Main"):
        self.observer = observer

    def notifyObserver(self, diststate: DistanceSensorState):
        self.observer.eventListener(diststate)

    def addSensor(self, distanceSensor: "DistanceSensor"):
        self.sensor = distanceSensor

    def updatedistState(self, dist_cm:float):
        """動作状態（self.state）を更新する
        """
        if self.diststate == DistanceSensorState.STANDBY:
            if dist_cm < self.threshold_dist:
                self.diststate = DistanceSensorState.HUMAN_IS_NEAR
            else:
                self.diststate = DistanceSensorState.HUMAN_IS_FAR
        else:
            if dist_cm < self.threshold_dist:
                self.diststate = DistanceSensorState.HUMAN_IS_NEAR
            else:
                self.diststate = DistanceSensorState.HUMAN_IS_FAR
        return self.diststate

    def __measure__(self):
        while True:
            dist_cm = self.sensor.measureSmooth()
            diststate = self.updatedistState(dist_cm)
            self.notifyObserver(diststate)
            time.sleep(0.5)  # 測定間隔を0.5秒ごととする

    def startMeasure(self):
        t = threading.Thread(target=self.__measure__)
        t.setDaemon(True)
        t.start()


# 物理ピン番号
TRIG = 11
ECHO = 13

class DistanceSensor:
    """センサを物理的にセットアップしたり、距離を測定したりする
    """
    def __init__(self):
        # センサーのセットアップ
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)

        GPIO.output(TRIG, GPIO.LOW)
        time.sleep(0.3)
        
        # 7回分の測定結果を格納するキューを作成
        self.distance_que = queue.Queue()
        for i in range(7):
            # キューに7回分の測定結果を格納
            self.distance_que.put(self.__measureRaw())


    def __del__(self):
        GPIO.cleanup()

    def __measureRaw(self):
        """センサーを用いて距離を測定する
        """
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
 
        while GPIO.input(ECHO) == 0:
            signaloff = time.perf_counter()

        while GPIO.input(ECHO) == 1:
            signalon = time.perf_counter()

        timepassed = signalon - signaloff
        distance = timepassed * 17000
        # 次の測定のため最低60ms待つ
        time.sleep(0.06)
        return distance


    def measureSmooth(self):
        """ 7回測定した内の中央値を返す
        """
        # キューから古い測定結果を1つ削除する
        self.distance_que.get()
        # 新たに1回分測定してキューに格納する
        self.distance_que.put(self.__measureRaw())
        # 中央値を返す
        return sorted(self.distance_que.queue)[3]
