__author__ = 'lucas'

# Cliente
import socket
import json

HOST='0.0.0.0' #coloca o host do servidor
PORT=9999

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
# arq=open('teste','rb')
s.sendall(json.dumps({"command":"reader","file":"logs/log.txt","master_server":"0.0.0.0"}).encode())
rest_string = ""
while True:
    data = s.recv(1024)
    data_list = (rest_string + data.decode()).split("\n")
    rest_string = data_list.pop()
    print(data_list)
    # print(l[l.index("userid=")+7:].replace("\"",""))
    if not data:
        break
    print(repr(data))
s.close()


# print('Received', repr(data))
# for i in arq:
#
#     # # s.send(json.dumps({"command":"reader","file":"logs/log.txt"}).encode())
#     # s.send(json.dumps({"command":"write","file":"logs/lucas","content":"linha1\nlinha2"}).encode())
# #
# # s.send(json.dumps({"command":"write","file":"logs/log.txt"}).encode())
#
# print("saindo...")
# arq.close()
# s.close()

