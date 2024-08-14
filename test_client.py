import socket

sock=socket.socket()
sock.connect(('localhost',9898))
sock.send(b'READ_DATA;1;DT1,DT2,DT3')
data=sock.recv(2048)
sock.close
print(data)