import socket as s

def result(id):
    print(id)
    return True

def operData(id):
    # sockObj=s.socket()
    # ip=s.gethostname()
    # numP=9898
    # sockObj.connect(ip, numP)
    # mess='READ_DATA;'+str(id)+';'+'Status_v9,Depth,Power,Speed,TimeBeforeStart,NSucYes,NSucTod,NSucTot'
    # sockObj.send(mess.encode())
    # data=sockObj.recv(2048)
    # answer=data.decode()
    # answer=answer.split(';')
    # if 'READ_DATA' in answer:
    #     dVals={}
    #     vals=answer[2].split(',')
    #     for i in vals:
    #         lVal=i.split('=')
    #         dVals[lVal[0]]=lVal[1]
    # return dVals
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
    mess='WRITE_DEVICE_SETTING'+';'+str(id)+';'+st
    sockObj.send(mess.encode())
    data=sockObj.recv(2048)
    answer=data.decode()
    answer=answer.split(';')
    if 'WRITE_DEVICE_SETTING' in answer:
        return 'Успешно! Подождите пока измененные уставки вступят в силу'
    else:
        return 'Возникла ошибка при передаче! Пожалуйста, повторите попытку'
