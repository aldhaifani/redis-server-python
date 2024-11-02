import socket

def main():
    # Create a server socket and bind it to localhost:6379
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    client, _ = server_socket.accept()  # wait for client

    data = client.recv(1024)  # receive data from client

    # Loop to receive data from client
    while data:
        if "PING" in data.decode():  # check if client sent PING
            client.send(b"+PONG\r\n")  # send PONG to client

        data = client.recv(1024)  # receive data from client

    client.close()  # close client connection

if __name__ == "__main__":
    main()