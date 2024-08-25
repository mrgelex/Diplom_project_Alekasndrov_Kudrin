import socket as s

def result(id):

    sockObj=s.socket()
    ip='localhost'
    numP=9898
    sockObj.connect((ip, numP))
    mess='STATUS_WRITE;'+str(id)
    sockObj.send(mess.encode())
    data=sockObj.recv(2048)
    answer=data.decode()
    answer=answer.split(';')
    mess
    if 'STATUS_WRITE' in answer:
        answer=answer[2].split(',')
        if 'COMPLETE' in answer:
            return True, 'Успешно!'
        elif 'ERROR_UNKNOWN_PARAM' in answer:
            return True, 'Возникла ошибка при записи! Пожалуйста, Пожалуйста, убедитесь в правильности введенных уставок'
        elif 'ERROR_TIMEOUT' in answer:
            return True, 'Возникла ошибка при передаче! Пожалуйста, повторите попытку'
        elif 'PROCESSING' in answer:
            return False, 'Подождите пока измененные уставки вступят в силу'

        
def convertType(lVal):
    if lVal[0] in ['NWires', 'WorkDepth', 'TmClearDelta', 'TmClearAbs', 'TmWaitWorkDepth',
                   'TmWaitLubr', 'LimPlugDown', 'TmWaitDatPro', 'DepthClearUst', 'TmClearUst',
                   'TmWaitECN', 'CollarDepth']:
        lVal[1]=int(lVal[1])
    elif lVal[0] in ['WorkSpeed', 'ManualSpeed', 'CollarSpeed']:
        lVal[1]=float(int(lVal[1])/10)
    elif lVal[0]=='EnUpECN':
        if lVal[1]=='1':
            lVal[1]=True
        else:
            lVal[1]=False
    
    return lVal

def operData(id, mod):
    sockObj=s.socket()
    ip='localhost'
    numP=9898
    sockObj.connect((ip, numP))
    if mod:
        valStr='Status_v9,Depth,Power,Speed,TimeBeforeStart,NSucYes,NSucTod,NSucTot'
    else:
        valStr='Username1,Username2,NWires,WorkDepth,WorkSpeed,TmClearDelta,TmClearAbs,TmWaitWorkDepth,TmWaitLubr,ManualSpeed,LimPlugDown,TmWaitDatPro,DepthClearUst,TmClearUst,TmWaitECN,EnUpECN,CollarSpeed,CollarDepth'
    mess='READ_DATA;'+str(id)+';'+valStr
    sockObj.send(mess.encode())
    data=sockObj.recv(2048)
    print(data)
    answer=data.decode()
    answer=answer.split(';')
    if 'READ_DATA' in answer:
        dVals={}
        vals=answer[2].split(',')
        for i in vals:
            if i=='NULL':
                if mod:
                    return {'Status_v9':'Нет связи','Depth':'Нет связи','Power':'Нет связи','Speed':'Нет связи','TimeBeforeStart':'Нет связи','NSucYes':'Нет связи','NSucTod':'Нет связи','NSucTot':'Нет связи'}
                else:
                    return {}
            lVal=i.split('=')
            if not mod:
                lVal=convertType(lVal)
            dVals[lVal[0]]=lVal[1]
        if mod:
            dVals['Speed']=int(dVals.get('Speed'))/10
            dVals['Status_v9']=int(dVals.get('Status_v9'))

    return dVals

def writeSP(id, sp):
    sockObj=s.socket()
    ip='localhost'
    numP=9898
    sockObj.connect((ip, numP))
    st=''
    for i in sp:
        if i =='EnUpECN':
            if sp.get(i):
                sp[i]=1
            else:
                sp[i]=0
        st=st+i+'='+str(sp.get(i))+','
    st=st.rstrip(',')
    mess='WRITE_DEVICE_SETTING;'+str(id)+';'+st
    sockObj.send(mess.encode())
    data=sockObj.recv(2048)
    answer=data.decode()
    answer=answer.split(';')
    if 'PROCESSING' in answer:
        return False, 'Подождите пока измененные уставки вступят в силу'
    elif 'ERROR_TIMEOUT' in answer:
        return True, 'Возникла ошибка при передаче! Пожалуйста, повторите попытку'
    elif 'ERROR_UNKNOWN_PARAM' in answer:
        return True, 'Возникла ошибка при проверке данных! Пожалуйста, убедитесь в правильности введенных уставок'
    elif 'ERROR ID DEVICE' in answer:
        return True, 'Устройство не найдено!'