import socket
import sys
import threading
import ssl


def main():
    global listen_port , buffer_size, max_conn

    try:
        listen_port = int(input("Enter a port to listen : "))
    except KeyboardInterrupt:
        sys.exit(0)

    max_conn = 5
    buffer_size = 8192

    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('',listen_port))
        s.listen(max_conn)
        print("[*] Server Started at [{}]".format(listen_port))
    except Exception as e:
        print(e)
        sys.exit(2)

    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size)
            data = data.decode()
            proxy_thread = threading.Thread(target=con_string,args=(conn,data,addr))
            proxy_thread.start()
        except KeyboardInterrupt:
            s.close()
            print("\n{*] Shutting Down")
            sys.exit(1)
    s.close()


def con_string(conn,data,addr):
    try:
        first_line = data.split("\n")[0]
        url = first_line.split(" ")[1]

        http_pos = url.find("://")
        if http_pos == -1 :
            temp = url
        else:
            temp = url[(http_pos+3):]

        port_pos = temp.find(":")
        webserver_pos = temp.find("/")

        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver=""
        port = -1

        if port_pos == -1 or webserver_pos < port_pos:
            port=80
            webserver = temp[:webserver_pos]
        else:
            port = int(temp[(port_pos+1):][:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        print(data)
        print(webserver)
        #print(addr)

        proxy_server(webserver, port, conn, data, addr)

    except Exception as e:
        print("c2")
        print(e)



def proxy_server(webserver, port, conn, data, addr):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # connect the client
        s.connect((webserver, 80))

        # ssl wrap the socket
        context = ssl.create_default_context()
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1
        context.options |= ssl.OP_NO_COMPRESSION
        cipher = 'DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:ECDHE-ECDSA-AES128-GCM-SHA256'
        context.set_ciphers(cipher)
        s = context.wrap_socket(s, server_hostname=webserver)


        s.send(data.encode())

        while True:
            #print("t1")
            reply = s.recv(buffer_size)
            #print("t2")
            if len(reply) > 0:
                #print("t3")
                conn.send(reply)
                print(reply.decode())
                #print("t4")
                dar = float(len(reply))
                dar = float(dar/1024)
                dar = "{}.3s".format(dar)
                print("[*] Request done: {} => {} <= {}".format(addr[0],dar,webserver))
            else:
                break
        s.close()
        conn.close()
    except Exception as e:
        print("c1")
        print(e)
        s.close()
        sys.exit(1)


if __name__ == "__main__":
    main()





