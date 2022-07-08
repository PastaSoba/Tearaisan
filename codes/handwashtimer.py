import time

class HandwashTimer:
    def __init__(self, tearaiTime):
        """
        argument:
            tearaiTime: 手洗いをしたとみなす時間（秒）
        """
        self.tearaiTime = tearaiTime

    def startTearai(self):
        # 手洗い開始時にこの関数を実行する
        self.startTime = time.time()

    def endTearai(self) -> bool:
        # 手洗い終了時にこの関数を実行する
        # 返り値は手洗い成功->True, 手洗い失敗->False
        self.endTime = time.time()
        return (self.endTime - self.startTime) > self.tearaiTime
