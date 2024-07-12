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
                request_data = data.decode().split(" ")
                if not data:
                    break
                request_path = request_data[1] 
                if request_path[0] == "/" and len(request_path)>1:
                    connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
                else:
                    connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

if __name__ == "__main__":
    main()
