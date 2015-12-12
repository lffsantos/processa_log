#coding:utf-8
import concurrent.futures
import socket
import _thread
import json
from collections import defaultdict
from uuid import UUID
from queue import Queue, Empty
import argparse

__author__ = 'lucas'

step = 0

class LogProcessor(object):

    def __init__(self, servers, log_dir):
        self.servers = servers
        self.path_save_log = "/tmp/[USERID]"
        self.log_dir = log_dir
        self.cookies = defaultdict(list)
        self.queue = Queue()

    def start_connections(self):
        print("Iniciando conexão!")
        self._socket_list = {}
        for k, v in self.servers.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((v, 9998))
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
                if count == len(self.servers):
                    break
            except Empty:
                pass

        print("log processado")


    def read_log(self, num_server):
        self._socket_list[num_server].sendall(json.dumps({"command":"reader","file":self.log_dir}).encode())
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
        global step
        data = {
            "command":"write",
            "file":self.path_save_log.replace("[USERID]",user_id),
            "content": data
        }

        step +=1
        if step%100 == 0:
            print("write_log...")
        self._socket_list[self.get_number_server_save_log(user_id)].sendall(json.dumps(data).encode()+b'\n')

    def get_number_server_save_log(self, user_id):

        token = int(UUID(user_id))%len(self.servers)
        return token


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--servers", type=str, required=True,
                        help="List of Servers to collect log. \n ex:\"teste1,teste2\"")
    parser.add_argument("-ld", "--log_dir", default="logs/log.txt",
                        help="location of log")

    args = parser.parse_args()
    list_servers = args.servers.split(",")
    print(list_servers)
    print("localização dos logs: " + args.log_dir)
    servers = {}

    for i in range(0,len(list_servers)):
        servers[i] = list_servers[i]

    log = LogProcessor(servers, args.log_dir)
    log.start_connections()
    log.start()



