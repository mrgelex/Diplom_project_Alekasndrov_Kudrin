import socket as s

def result(id):

    sockObj=s.socket()
    ip=s.gethostname()
    numP=9898
    sockObj.connect(ip, numP)
    mess='STATUS_WRITE;'+str(id)
    sockObj.send(mess.encode())
    data=sockObj.recv(2048)
    answer=data.decode()
    answer=answer.split(';')
    mess
    if 'STATUS_WRITE' in answer:
        answer=answer[2].split(',')
        if 'OK' in answer:
            return True, 'Успешно!'
        elif 'ERROR' in answer:
            return True, 'Возникла ошибка при записи! Пожалуйста, повторите попытку '
        else:
            return False
        
def convertType(lVal):
    if lVal[1]=='NULL':
        lVal[1]=None
        return lVal
    if lVal[0] in ['NWires', 'WorkDepth', 'TmClearDelta', 'TmClearAbs', 'TmWaitWorkDepth',
                   'TmWaitLubr', 'LimPlugDown', 'TmWaitDatPro', 'DepthClearUst', 'TmClearUst',
                   'TmWaitECN', 'CollarDepth']:
        lVal[1]=int(lVal[1])
    elif lVal[0] in ['WorkSpeed', 'ManualSpeed', 'CollarSpeed']:
        lVal[1]=float(lVal[1])
    elif lVal[0]=='TmWaitECN':
        if lVal[1]=='1':
            lVal[1]=True
        else:
            lVal[1]=False
    
    return lVal

def operData(id, mod):
    sockObj=s.socket()
    ip=s.gethostname()
    numP=9898
    sockObj.connect(ip, numP)
    if mod:
        valStr='Status_v9,Depth,Power,Speed,TimeBeforeStart,NSucYes,NSucTod,NSucTot'
    else:
        valStr='Username2,NWires,WorkDepth,WorkSpeed,TmClearDelta,TmClearAbs,TmWaitWorkDepth,TmWaitLubr,ManualSpeed,LimPlugDown,TmWaitDatPro,DepthClearUst,TmClearUst,TmWaitECN,EnUpECN,CollarSpeed,CollarDepth'
    mess='READ_DATA;'+str(id)+';'+valStr
    sockObj.send(mess.encode())
    data=sockObj.recv(2048)
    answer=data.decode()
    answer=answer.split(';')
    if 'READ_DATA' in answer:
        dVals={}
        vals=answer[2].split(',')
        for i in vals:
            lVal=i.split('=')
            if lVal[1]=='NULL' and mod:
                lVal[1]='Нет связи'
            elif not mod:
                lVal=convertType(lVal)
            dVals[lVal[0]]=lVal[1]
    return dVals
    print(id)
    return {'Status_v9': '2', 'Depth': '3', 'Power': '1', 'Speed': '5', 'TimeBeforeStart': '7', 'NSucYes': '1', 'NSucTod': '0', 'NSucTot': '8'}

def writeSP(id, sp):
    sockObj=s.socket()
    ip=s.gethostname()
    numP=9898
    sockObj.connect(ip, numP)
    st=''
    for i in sp:
        st=st+i+'='+str(sp.get(i))+','
    st=st.rstrip(',')
    mess='WRITE_DEVICE_SETTING;'+str(id)+';'+st
    sockObj.send(mess.encode())
    data=sockObj.recv(2048)
    answer=data.decode()
    answer=answer.split(';')
    if 'WRITE_DEVICE_SETTING' in answer:
        return 'Подождите пока измененные уставки вступят в силу'
    else:
        return 'Возникла ошибка при передаче! Пожалуйста, повторите попытку'
