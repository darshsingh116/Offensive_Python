import sys
import socket
import threading
from hexdump import hexdump


def receive_from(connection):
    buffer = ""
    # We set a 2 second timeout; depending on your
    # target, this may need to be adjusted
    connection.settimeout(15)
    # keep reading into the buffer until
    # there's no more data
    # or we time out
    try:
        print("c4")
        data = connection.recv(4096)
        buffer = data
        print("first data")
        print(data.decode())
        while(True):
            print("c4.1")
            data = connection.recv(4096)
            print("c4.2")
            print("nth data")
            print(data.decode())
            if(not data):
                print("BREAK")
                break
            buffer = buffer + data

    except Exception as e:
        print("c5")
        print(e)
        pass
    print("asss")
    #print(buffer.decode())
    print("asshol")
    print(type(buffer))
    #####################   BUFFER IS BEING STR NOT BYTES FIX!!
    return buffer
# modify any requests destined for the remote host
def request_handler(buffer):
    # perform packet modifications
    return buffer

# modify any responses destined for the local host
def response_handler(buffer):
    # perform packet
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    # connect to the remote host
    print("c1")
    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))
    print("c2")
    # receive data from the remote end if necessary
    if(receive_first):
        remote_buffer = receive_from(remote_socket)
        print("c6")
        #remote_buffer = remote_buffer.decode()
        print(type(remote_buffer))
        ##hexdump(remote_buffer)
        # send it to our response handler
        ##remote_buffer = response_handler(remote_buffer)
    # if we have data to send to our local client, send it
        if(len(remote_buffer)):
            print( "[<==] Sending %d bytes to localhost." % len(remote_buffer))
            client_socket.send(remote_buffer)
    # now lets loop and read from local,
    # send to remote, send to local
    # rinse, wash, repeat
    while(True):
        # read from local host
        local_buffer = receive_from(client_socket)
        if(len(local_buffer)):
            print( "[==>] Received %d bytes from localhost." % len(local_buffer))
            ##hexdump(local_buffer)
            # send it to our request handler
            local_buffer = request_handler(local_buffer)
            print("lcl buff~~")
            print(local_buffer.decode())
            # send off the data to the remote host
            remote_socket.send(local_buffer)
            print( "[==>] Sent to remote.")
            # receive back the response
            remote_buffer = receive_from(remote_socket)
            print(remote_buffer.decode())
            print("yemsssss")
        if(len(remote_buffer)):
            print( "[<==] Received %d bytes from remote." % len(remote_buffer))
            ##hexdump(remote_buffer)
            # send to our response handler
            remote_buffer = response_handler(remote_buffer)
            # send the response to the local socket
            client_socket.send(remote_buffer)
            print( "[<==] Sent to localhost.")

        # if no more data on either side, close the connections
        if(not len(local_buffer) or not len(remote_buffer)):
            client_socket.close()
            remote_socket.close()
            print( "[*] No more data. Closing connections.")
            break



def server_loop(local_host,local_port,remote_host,remote_port,receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((local_host,local_port))
    except:
        print( "[!!] Failed to listen on %s:%d" % (local_host,local_port))
        print( "[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)
    print("[*] Listening on %s:%d" % (local_host,local_port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        # print out the local connection information
        print("[==>] Received incoming connection from %s:%d" % (addr[0],addr[1]))
        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port,receive_first))
        proxy_thread.start()


def main():
    # no fancy command-line parsing here
    if len(sys.argv[1:]) != 5:
        print( "Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print( "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
        # setup local listening parameters
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    # setup remote target
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    # this tells our proxy to connect and receive data
    # before sending to the remote host
    receive_first = sys.argv[5]
    if("True" in receive_first):
        receive_first = True
    else:
        receive_first = False
    # now spin up our listening socket
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)


main()
