import socket
import time

host='192.168.1.39'
port=1337
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
st='connection done'
byt=st.encode()
s.send(byt)
s.send(byt)
#data, addr = s.recvfrom(4096)

time.sleep(1)
#print(data)

s.send(byt)

