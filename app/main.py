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
                # GET /echo/abc HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n
                request_data = data.decode().split(" ")

                if not data:
                    break

                # /foobar/1.2.3\r\n or /echo/abc or /abc or /
                # ['', 'foobar', '1.2.3\r\n']
                request_path = request_data[1].split("/")
                
                check_UserAgent = request_path[2] #1.2.3\r\n

                if len(request_path) >= 3 and request_path[1] == "echo":
                    content = request_path[2]
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
                    connection.sendall(response.encode())

                elif check_UserAgent[-4:] == "\r\n":
                    raw_agent = request_data[1] # /foobar/1.2.3\r\n
                    user_agent = raw_agent[1:13] # foobar/1.2.3 

                    user_agent_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
                    connection.sendall(user_agent_response.encode())

                elif request_path[1] != '':
                    connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
                
                else:
                    connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

if __name__ == "__main__":
    main()
