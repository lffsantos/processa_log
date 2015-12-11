import socket
import json
import _thread
import traceback
from queue import Queue, Empty
import time

class SocketServer(object):

    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 9999

        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(10)
        self.conn, addr = self.sock.accept()
        self.queue = Queue()

    def create_conn_sock(self, server):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host,self.port))
        return s

    def run(self):
        rest_msg = ""
        try:
            while True:
                try:
                    item = self.queue.get_nowait()
                    time.sleep(3)
                    print("stop")
                    self.conn.sendall("stop".encode())
                except Empty:
                    dados= self.conn.recv(1024)
                    if dados:
                        data_list = (rest_msg + dados.decode()).split("\n")
                        if len(data_list) > 1:
                            rest_msg = data_list.pop()
                        for data in data_list:
                            try:
                                dados = json.loads(data)
                                if dados:
                                    if dados.get("command") == "reader":
                                        _thread.start_new_thread(self.read_file, (dados["file"],))
                                    elif dados.get("command") == "write":
                                        _thread.start_new_thread(self.write_file, (dados["file"], dados["content"],))
                            except:
                                print(data)
                                traceback.format_exc()

        except:
            print(traceback.format_exc())
            self.conn.close()

    def read_file(self, file):
        with open(file, 'r') as line:
            for l in line:
                self.conn.sendall(l.encode())

        self.queue.put_nowait(0)


    def write_file(self, file_path, content):
        file = open(file_path, "a")
        file.write(content + "\n")
        file.close()


if __name__ == '__main__':

    print("Server Runner...")
    conn = SocketServer()
    conn.run()