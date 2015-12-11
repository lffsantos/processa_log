import concurrent.futures
import socket
import _thread
import json
from collections import defaultdict
from uuid import UUID
from queue import Queue, Empty

__author__ = 'lucas'


class LogProcessor(object):

    def __init__(self, servers):
        self.servers = servers
        self.path_log = "/tmp/[USERID]"
        self.cookies = defaultdict(list)
        self.queue = Queue()

    def start_connections(self):
        print("Iniciando conexão!")
        self._socket_list = {}
        for k, v in self.servers.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((v, 9999))
            self._socket_list[k] = sock
        print("conexão realizada!")

    def start(self):
        print("iniciando processamento dos logs")

        def run(num_server):
            _thread.start_new_thread(self.read_log(num_server))

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for num_server, ip_server in self.servers.items():
                executor.submit(run, num_server)

        count = 0
        while True:
            try:
                item = self.queue.get_nowait()
                count +=1
                if count == len(servers):
                    break
            except Empty:
                pass

        print("log processado")


    def read_log(self, num_server):
        self._socket_list[num_server].sendall(json.dumps({"command":"reader","file":"logs/log.txt"}).encode())
        rest_string = ""
        while True:
            data = self._socket_list[num_server].recv(1024)
            if not data or data == b'stop':
                break
            data_list = (rest_string + data.decode()).split("\n")
            rest_string = data_list.pop()
            self.parser_log(data_list)

        self.queue.put_nowait(0)

    def parser_log(self,data_list):

        for data in data_list:
            user_id = data[data.index("userid=")+7:].replace("\"","")
            self.write_user_log(user_id, data)


    def write_user_log(self, user_id, data):
        data = {
            "command":"write",
            "file":self.path_log.replace("[USERID]",user_id),
            "content": data
        }
        print("enviando")
        self._socket_list[self.get_number_server_save_log(user_id)].sendall(json.dumps(data).encode()+b'\n')
        print("-----")

    def get_number_server_save_log(self, user_id):

        token = int(UUID(user_id))%len(self.servers)
        return token

    def __close_sockets(self):
        for list in self._socket_list:
            for sock in list:
                try:
                    sock.close()
                except:
                    pass


if __name__ == '__main__':

    # servers = {
    #     0: 'localhost',
    #     1: '52.90.110.61',
    #     3: '52.90.110.40',
    #     4: '52.90.114.235'
    # }
    servers = {
        0: '52.90.110.61',
        1: '54.152.179.63'
    }

    log = LogProcessor(servers)
    log.start_connections()
    log.start()


