import subprocess

class MusicPlayer:
    """BGMやSEの再生、中断を行う
    クラスの外側からは、このクラスがシェルスクリプトを実行していることが
    見えないようにする
    """
    def __init__(self):
        # 現在再生中の曲のファイルパスを含んでいる集合
        self.playlist = set()

    def play(self, filename:str):
        self.playlist.add(filename)
        cmd = ["/home/pi/codes/start_music.sh", filename]
        subprocess.call(cmd)

    def stop(self, filename:str):
        self.playlist.remove(filename)
        cmd = ["/home/pi/codes/stop_music.sh", filename]
        subprocess.call(cmd)
    
    def stopall(self):
        # 再生している全てのBGMを停止する
        for filename in self.playlist:
            cmd = ["/home/pi/codes/stop_music.sh", filename]
            subprocess.call(cmd)
        self.playlist.clear()