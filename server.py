import socket
#import time
import sqlite3 as sl
import device
from threading import Thread
import TextWrapper
#from queue import Empty, Queue

pathDB='web_interface/Logs.db'

class Server:
    def __init__(self,text):
        self.enable=True
        self.text=text
        
    def Start(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT device_id FROM DEVICE""")
            self.device_list=cursor.fetchall()
        self.dev={}
        for s in self.device_list:
            self.dev[s[0]]=device.Device(s[0],2,self.text)
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
        sock.settimeout(5)
        sock.bind(('localhost',9898))
        sock.listen(10)
        print("Start server socket", file=TextWrapper.TextWrapper(self.text))
        while self.enable:
            try:
                conn,addr=sock.accept()
                data=conn.recv(2048)
                print(data)
                data=data.decode()
                self.cmd=data.split(sep=";")
                if self.cmd[0]=="READ_DATA":
                    try:
                        resp=self.dev[int(self.cmd[1])].GetData(self.cmd[2])
                        snd="READ_DATA;"+self.cmd[1]+";"+resp
                        conn.send(snd.encode())
                    except:
                        snd="READ_DATA;"+self.cmd[1]+";NULL"
                        conn.send(snd.encode())
                elif self.cmd[0]=="WRITE_DEVICE_SETTING":
                    try:
                        self.dev[int(self.cmd[1])].WriteData(self.cmd[2])
                        snd="WRITE_DEVICE_SETTING;"+self.cmd[1]+";PROCESSING"
                        conn.send(snd.encode())
                    except:
                        snd="WRITE_DEVICE_SETTING;"+self.cmd[1]+";ERROR ID DEVICE"
                        conn.send(snd.encode())
                elif self.cmd[0]=="STATUS_WRITE":
                    try:
                        resp=self.dev[int(self.cmd[1])].GetStatusWrite(self.cmd[2])
                        snd="STATUS_WRITE;"+self.cmd[1]+";"+resp
                        conn.send(snd.encode())
                    except:
                        snd="STATUS_WRITE;"+self.cmd[1]+";ERROR ID DEVICE"
                        conn.send(snd.encode())
                else:
                    snd="UNKNOWN_COMMAND: "+data
                    conn.send(snd.encode())
            except:
                pass
        try:
            conn.close()
        except:
            pass
        print("Stop server socket", file=TextWrapper.TextWrapper(self.text))
    
#S=Server()
#S.Start()
#time.sleep(30)
#S.Stop()
