import socket
#import time
import sqlite3 as sl
import device
from threading import Thread
#from queue import Empty, Queue

pathDB='Logs.db'

class Server:
    def __init__(self):
        self.enable=True
        
    def Start(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT device_id FROM DEVICE""")
            self.device_list=cursor.fetchall()
        self.dev={}
        for s in self.device_list:
            print("Start id="+str(s[0]))
            self.dev[s[0]]=device.Device(s[0],2)
            self.dev[s[0]].Start()
        self.enable=True
        th=Thread(target=self.Thread)
        th.daemon=True
        th.start()
         
    def Stop(self):
        self.enable=False
        for s in self.dev:
            self.dev[s].Stop()
        
    def Thread(self):
        sock=socket.socket()
        sock.bind(('localhost',9898))
        sock.listen(10)
        while self.enable:
            conn,addr=sock.accept()
            data=conn.recv(2048)
            self.cmd=data.split(sep=b";")
            if self.cmd[0]==b"READ_DATA":
                try:
                    resp=self.dev[int(self.cmd[1])].GetData(self.cmd[2])
                    conn.send(b"READ_DATA;"+self.cmd[1]+b";"+resp)
                except:
                    conn.send(b"READ_DATA;"+self.cmd[1]+b";NULL")
            elif self.cmd[0]==b"WRITE_DEVICE_SETTING":
                pass
            elif self.cmd[0]==b"STATUS_WRITE":
                pass
            else:
                conn.send(b"UNKNOWN_COMMAND: "+data)
            conn.close()
    
#S=Server()
#S.Start()
#time.sleep(30)
#S.Stop()
