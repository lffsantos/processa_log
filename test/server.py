# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(2)
print('wait')
conn, addr = s.accept()
print('Connected by', addr)
while True:
    data = conn.recv(1024)
    if data:
        conn.sendall(b'lucas')
        conn, addr = s.accept()
        print("conectou")
conn.close()