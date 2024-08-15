import socket

sock=socket.socket()
sock.connect(('localhost',9898))
sock.send(b'WRITE_DEVICE_SETTING;1;WorkDepth=200')
data=sock.recv(2048)
sock.close
print(data)