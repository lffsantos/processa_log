from uuid import uuid4
from datetime import date, timedelta, datetime
from random import random, randint
__author__ = 'lucas'


log_ex = "177.126.180.83 - - [DATA] \"GET /meme.jpg " \
         "HTTP/1.1\" 200 2148 \"-\"userid=USERID\""

if __name__ == '__main__':


    lista_cokies = []

    data = datetime.now()
    for i in range(100):
        lista_cokies.append(str(uuid4()))
    for i in range(1,5):
        file = open("log"+str(i)+".txt","w")
        lista_logs  = []
        for i in range(1000):
            aux = randint(0, 99)
            data = data + timedelta(seconds=1)
            log = log_ex.replace("DATA",data.strftime("%d/%b/%Y:%H:%M:%S") + " -0300").replace("USERID",lista_cokies[aux])
            lista_logs.append(log)
            lista_logs.append("\n")

        file.writelines(lista_logs)
        file.close()
