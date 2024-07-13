# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    with socket.create_server(("localhost", 4221), reuse_port=True) as server_socket:
    # server_socket.accept() # wait for client
        connection, address = server_socket.accept()

        with connection:
            while True:
                # recieves data from the connection
                data = connection.recv(1024)
                # decode data in utf-8 format by default

                # 3. recieved GET /echo/abc HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n
                request_data = data.decode().split(" ")
                
                if not data:
                    break
                request_path = request_data[2]
                content = request_path[6:]
                content_type = type(content)
                content_length = len(request_path[6:])
                response = "HTTP/1.1 200 OK\r\nContent-Type: {}/plain\r\nContent-Length: {}\r\n\r\n{}".format(content_length, content, content_type)

                if request_path[0] == "/" and len(request_path)>1 and request_path[1:5] != "echo":
                    connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
                elif request_path[0:6] == "/echo/":
                    connection.sendall(response.encode())
                else:
                    connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

if __name__ == "__main__":
    main()
