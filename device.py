import pymodbus.client as modbusClient
from pymodbus import ModbusException
from pymodbus import Framer
import sqlite3 as sl
from datetime import datetime
from threading import Thread
from queue import Empty, Queue
import time
import TextWrapper

pathDB='web_interface/Logs.db'

class Device:
    def __init__(self,id_device,per,text):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT * FROM DEVICE WHERE device_id="""+str(id_device))
            answear=cursor.fetchall()
        self.id_device=answear[0][0]
        self.folder_id=answear[0][1]
        self.name_user=answear[0][2]
        self.IMEI=answear[0][3]
        self.description=answear[0][4]
        self.IP=answear[0][5]
        self.port=answear[0][6]
        if answear[0][7]=="true":
            self.modbus_over_tcp=True
        else:
            self.modbus_over_tcp=False
        self.add_pr200=answear[0][8]
        self.add_tr16=answear[0][9]
        self.add_inv=answear[0][10]
        self.type_inv=answear[0][11]
        self.GMT=answear[0][12]
        if answear[0][13]=="true":
            self.enable=True
        else:
            self.enable=False
        self.adt1=0
        self.adt2=0
        self.adt3=0
        self.per=per
        self.command=""
        self.signal_write=False
        self.signal_wu=""
        self.text=text
        
    def Start(self):
        self.ex_stop=False
        if self.enable:
            th=Thread(target=self.Thread)
            th.start()
        
    def Stop(self):
        self.ex_stop=True
        
    def ReadData64(self):
        try:
            response = self.client.read_holding_registers(address=512,count=64,slave=self.add_pr200)
            return response
        except ModbusException as exc:
            print(str(self.name_user)+": connect timeout", file=TextWrapper.TextWrapper(self.text))
            return exc
    
    def WriteSettings30(self):
        self.dict_u={}
        v9024u=["NWires","WorkDepth","WorkSpeed","TmClearDelta","TmClearAbs","TmWaitWorkDepth","TmWaitLubr","DepthClearUst","TmClearUst","TmIgnECN","TmWaitECN","EnUpECN",
               "ManualSpeed","CollarSpeed","CollarDepth","res1","res2","HLimService","LimPlugUp","LimPlugDown","TmWaitDatPro","DeltaTmWaitDatPro","TmWaitDatZak","Overload",
               "TmOverload","TmDpS1","TmDpS2","TmDpS3","TmDpS4","TmDelayDay"]
        for s in v9024u:
            try:
                self.dict_u[s]=self.dict_write[s]
            except:
                try:
                    self.dict_u[s]=self.dict_resp[s]
                except:
                    print(str(self.name_user)+": unknown setting", file=TextWrapper.TextWrapper(self.text))
                    self.signal_wu="ERROR UNKNOWN PARAM"
                    break
        if self.signal_wu=="PROCESSING":
            regs=[]
            for s in self.dict_u:
                regs.append(self.dict_u[s])
            try:
                responce=self.client.write_registers(address=528,values=regs,slave=self.add_pr200)
                self.signal_wu="COMPLETE"
                return responce
            except ModbusException as exc:
                print(str(self.name_user)+": write error", file=TextWrapper.TextWrapper(self.text))
                self.signal_wu="ERROR TIMEOUT"
                return exc
    
    def CheckVersion(self,resp):
        v9012=["DT1","DT2","DT3","Status_v9","Depth","Power","AI2","StringStatus","Status_v5","TimeBeforeStart","Depth2","Speed","Power2","NSucYes","NSucTod","NSucTot",
               "NWires","WorkDepth","WorkSpeed","TmClearDelta","TmClearAbs","TmWaitWorkDepth","TmWaitLubr","DepthClearUst","TmClearUst","TmIgnECN","TmWaitECN","EnUpECN",
               "ManualSpeed","CollarSpeed","CollarDepth","res1","res2","HLimService","LimPlugUp","LimPlugDown","TmWaitDatPro","DeltaTmWaitDatPro","TmWaitDatZak","Overload",
               "TmOverload","TmWaitAlarmDat","TmWaitEM","res3","res4","res5","Pot485","BitDat485","PowINV485","ControlWord_v5","SpeedINV_v5","BitMask_v5","ArcDT1","ArcDT2",
               "ArcDT3","ArcStatus","ArcDepth","ArcPower","ArcAI2","ArcStringStatus","Username1","Username2","DistControl","Verion"]
        v9024=["DT1","DT2","DT3","Status_v9","Depth","Power","AI2","StringStatus","Status_v5","TimeBeforeStart","Depth2","Speed","Power2","NSucYes","NSucTod","NSucTot",
               "NWires","WorkDepth","WorkSpeed","TmClearDelta","TmClearAbs","TmWaitWorkDepth","TmWaitLubr","DepthClearUst","TmClearUst","TmIgnECN","TmWaitECN","EnUpECN",
               "ManualSpeed","CollarSpeed","CollarDepth","res1","res2","HLimService","LimPlugUp","LimPlugDown","TmWaitDatPro","DeltaTmWaitDatPro","TmWaitDatZak","Overload",
               "TmOverload","TmDpS1","TmDpS2","TmDpS3","TmDpS4","TmDelayDay","Pot485","BitDat485","PowINV485","ControlWord_v5","SpeedINV_v5","BitMask_v5","ArcDT1","ArcDT2",
               "ArcDT3","ArcStatus","ArcDepth","ArcPower","ArcAI2","ArcStringStatus","Username1","Username2","DistControl","Verion"]
        if resp.registers[63]<9024:
            self.dict_ver=v9012
        if resp.registers[63]>=9024:
            self.dict_ver=v9024
        i=0
        self.dict_resp={}
        for name in self.dict_ver:
            self.dict_resp[name]=resp.registers[i]
            i+=1
        if self.dict_resp["Depth"]>32767:
            self.dict_resp["Depth"]=self.dict_resp["Depth"]-65536
        if self.dict_resp["ArcDepth"]>32767:
            self.dict_resp["ArcDepth"]=self.dict_resp["ArcDepth"]-65536 
        str_list=("DT1","DT2","DT3","ArcDT1","ArcDT2","ArcDT3")
        for s in str_list:
            self.dict_resp[s]=str(self.dict_resp[s]).zfill(4)
        return self.dict_resp
        
    def WriteTimeLog(self,dr):
        dt_dev="20"+dr["DT1"][0:2]+"-"+dr["DT1"][2:4]+"-"+dr["DT2"][0:2]+" "+dr["DT2"][2:4]+":"+dr["DT3"][0:2]+":"+dr["DT3"][2:4]
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""INSERT INTO LOG_TIME (device_id, timestamp_loc, timestamp_dev, GMT, status, depth, power, status_string) 
                           VALUES ('"""+str(self.id_device)+"""', '"""+str(self.dt_local)+"""', '"""+str(dt_dev)+"""', 
                           '"""+str(self.GMT)+"""', """+str(dr["Status_v9"])+""", """+str(dr["Depth"])+""", 
                           """+str(dr["Power"])+""", '"""+str(dr["StringStatus"])+"""')""")
            con.commit()
            cursor.close()
        
    def WriteEventLog(self,dr):
        if self.adt1 != dr["ArcDT1"] or self.adt2 != dr["ArcDT2"] or self.adt3 != dr["ArcDT3"]:
            dt_dev="20"+dr["ArcDT1"][0:2]+"-"+dr["ArcDT1"][2:4]+"-"+dr["ArcDT2"][0:2]+" "+dr["ArcDT2"][2:4]+":"+dr["ArcDT3"][0:2]+":"+dr["ArcDT3"][2:4]
            con = sl.connect(pathDB)
            with con:
                cursor=con.cursor()
                cursor.execute("""INSERT INTO LOG_EVENT (device_id, timestamp_loc, timestamp_dev, GMT, status, depth, power, status_string) 
                               VALUES ('"""+str(self.id_device)+"""', '"""+str(self.dt_local)+"""', '"""+str(dt_dev)+"""', 
                               '"""+str(self.GMT)+"""', """+str(dr["ArcStatus"])+""", """+str(dr["ArcDepth"])+""", 
                               """+str(dr["ArcPower"])+""", '"""+str(dr["ArcStringStatus"])+"""')""")
                con.commit()
                cursor.close()
            self.adt1=dr["ArcDT1"]
            self.adt2=dr["ArcDT2"]
            self.adt3=dr["ArcDT3"]
            
    def Thread(self):
        self.client = modbusClient.ModbusTcpClient(host=self.IP,port=self.port,framer=Framer.SOCKET,timeout=2)
        self.client.connect()
        while not self.ex_stop:
            t=time.time()
            rr=self.ReadData64()
            self.dt_local=datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            print(self.dt_local+" "+str(self.name_user)+": "+str(rr), file=TextWrapper.TextWrapper(self.text))
            if not rr.isError():  
                dr=self.CheckVersion(rr)
                self.WriteTimeLog(dr)
                self.WriteEventLog(dr)
            while t+self.per>time.time():
                time.sleep(1)
                if self.signal_write:
                    self.WriteSettings30()
        self.client.close()
        
    def GetData(self, req):
        srq=req.split(sep=",")
        rsp=""
        for s in srq:
            rsp=rsp+s+"="+str(self.dict_resp[s])+","
        rsp=rsp.rstrip(",")
        return rsp
    
    def WriteData(self, req):
        srq=req.split(sep=",")
        self.dict_write={}
        for s in srq:
            a=s.split("=")
            self.dict_write[a[0]]=int(a[1])
        self.signal_write=True
        self.signal_wu="PROCESSING"
        
    def GetStatusWrite(self):
        return self.signal_wu
        
            
        
#D=Device("1")     
#D.Start()
#time.sleep(30)
#D.Stop()