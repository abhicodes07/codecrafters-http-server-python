# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client
    connection, address = server_socket.accept()

    with connection:
        while True:
            # recieves data from the connection
            data = connection.recv(1024)
            # print(f"Received Data: {data} ")

            # decode data in utf-8 format by default
            request_data = data.decode().split("\r\n")
            # print(f"Decoded Data: {decode_data}")

            if not data:
                break

            request_path = request_data[0].split(" ") 
            # print(f"Requested Path: {request_path}")
            
            request_string = request_path[1].split()
            # Check condtion
            if request_string[0] == "/":
                connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
            elif request_string[0] != "/":
                connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

if __name__ == "__main__":
    main()
