import socket
import json
import traceback
from queue import Queue, Empty
import time

class SocketServer(object):

    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 9998
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(10)
        self.conn, addr = self.sock.accept()
        self.queue = Queue()

    def run(self):
        rest_msg = ""
        try:
            while True:
                try:
                    item = self.queue.get_nowait()
                    time.sleep(3)
                    print("stop")
                    self.conn.sendall("stop".encode())
                    self.conn, addr = self.sock.accept()
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
                                        self.read_file(dados["file"])
                                    elif dados.get("command") == "write":
                                        print("write")
                                        self.write_file(dados["file"], dados["content"])
                            except:
                                self.conn.close()
                                print(traceback.format_exc())


        except:
            self.conn.close()
            print(traceback.format_exc())


    def read_file(self, file):
        with open(file, 'r') as line:
            for l in line:
                self.conn.sendall(l.encode())

        self.queue.put_nowait(0)


    def write_file(self, file_path, content):
        file = open(file_path, "a")
        file.write(content + "\n")
        print(content)
        file.close()


if __name__ == '__main__':

    print("Server Runner...")
    try:
        conn = SocketServer()
        print("client connected")
        conn.run()
    finally:
        conn.sock.close()