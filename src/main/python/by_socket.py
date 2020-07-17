# flick_kb_receiver.py
import sys
import time
import socket
import pyautogui
import threading
#import pyperclip
"""
def type_text(text):
    # 与えた文字を入力（クリップボードにコピー＆ペースト）
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    return True

def type_backspace():
    pyautogui.typewrite(["backspace"])
    return True

def type_enter():
    pyautogui.typewrite(["enter"])
    return True
"""
class Receiver():
    def __init__(self, port=8888, ipaddr=None, set_daemon=True, log_function= None):
        """
        受信側

        Parameters
        ----------
        port : int
            使用するポート番号
        ipaddr : None or str
            受信側PCのIPアドレス．Noneで自動取得．
        set_daemon : bool
            スレッドをデーモン化するか．受信部スレッド終了を待たずにメインスレッドを停止させる．
        """
        if(ipaddr is None):
            host = socket.gethostname()
            ipaddr = socket.gethostbyname(host)
        self.ipaddr = ipaddr
        self.port = port
        self.set_daemon = set_daemon
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.loopflag = False
        self.log_function = log_function
        print("ip:{0} port:{1}".format(self.ipaddr, self.port))

    def loop(self):
        self.sock.settimeout(0.5)
        self.sock.bind((self.ipaddr, self.port))
        self.sock.listen(1)
        print("start listening...")
        while(self.loopflag):
            try:
                conn, addr = self.sock.accept()
            except socket.timeout:
                continue
            if self.log_function is None:
                print("accepted")
            else:
                self.log_function("conected")

                print("accepted")
            with conn:
                while(self.loopflag):
                    # print("waiting...")
                    data = conn.recv(1024)
                    print(data)
                    if(not data):
                        break
                    else:
                        text = data.decode("utf-8")
                        print(">", text)
                        if text =="L":
                            pyautogui.hotkey("ctrl", "winleft", "left")
                            print("L")
                        if text =="R":
                            pyautogui.hotkey("ctrl", "winleft", "right")
                            print("R")

    def start_loop(self):
        self.loopflag = True
        self.thread = threading.Thread(target=self.loop)
        if(self.set_daemon):
            self.thread.setDaemon(True)
        self.thread.start()
        print("start_thread")

    def stop_loop(self):
        print("stop loop")
        self.loopflag = False
        time.sleep(0.6)  # socketがtimeoutするまで待つ
        if(not self.set_daemon):
            print("waiting to stop client...")  # 送信側が停止するのを待つ
            self.thread.join()
        print("stop_thread")

    def close_sock(self):
        self.sock.close()
        print("socket closed")

def main():
    # コマンドライン引数
    ipaddr = None
    args = sys.argv
    if(len(args)<=1):
        print("Usage: flick_kb_receiver [PORT] [IP (optional)]")
        sys.exit()
    elif(len(args)==2):
        port = int(args[1])
    else:
        port = int(args[1])
        ipaddr = args[2]

    # メイン処理
    receiver = Receiver(port=port, ipaddr=ipaddr)
    receiver.start_loop()
    while True:
        stopper = input()
        if(stopper=="s"):
            receiver.stop_loop()
            break
    receiver.close_sock()

if __name__=="__main__":
    main()