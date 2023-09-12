import socket
import ssl

target_host = "www."
target_port = 443

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect the client
client.connect((target_host, target_port))

# ssl wrap the socket
context = ssl.create_default_context()
client = context.wrap_socket(client, server_hostname=target_host)

client.send(
    f"GET /xyz/../service/ HTTP/1.1\r\nHost:{target_host}\r\n\r\n".encode())

# receive some data
response = b''
while True:
    data = client.recv(4096)
    print(f'receiving {len(data)} bytes data...')
    print(response.decode())
    response += data
    if not data:
        client.close()
        break

http_response = repr(response)
http_response_len = len(http_response)

# display the response
print(f"http_response_len={http_response_len}, http_response={http_response}")
