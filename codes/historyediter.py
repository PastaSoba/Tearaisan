import json

class HistoryEditer:
    filepath = "/home/pi/public_html/history.txt"

    @staticmethod
    def loadjson() -> dict:
        file = open(HistoryEditer.filepath, "r")
        lst = list(map(int, file.read().split(",")))
        j = dict()
        j["success"] = lst[0]
        j["failure"] = lst[1]
        file.close()
        return j

    @staticmethod
    def recordjson(dic: dict) -> None:
        file = open(HistoryEditer.filepath, "w")
        lst = "{},{}".format(dic["success"], dic["failure"])
        file.write(lst)
        file.close()
