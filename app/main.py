# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    with socket.create_server(("localhost", 4221), reuse_port=True) as server_socket:
    # server_socket.accept() # wait for client
        connection, address = server_socket.accept()

        with connection:
            while True:
                # recieves data from the connection
                data = connection.recv(1024)
                if not data:
                    break

                # decode data in utf-8 format by default
                # GET /echo/abc HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n
                # GET /user-agent HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: mango/grape-grape\r\n\r\n
                request_data = data.decode().split(" ")

                # /user-agent or /echo/abc or /abc or /
                request_path = request_data[1].split("/")
                
                # check_UserAgent = request_path[1] # user-agent

                if len(request_path) >= 3 and request_path[1] == "echo":
                    content = request_path[2]
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
                    connection.sendall(response.encode())

                elif request_path == "user-agent":
                    raw_agent = request_data[4].split("\r\n") # mango/grape-grape\r\n\r\n
                    user_agent = raw_agent[0] # mango/grape-grape 

                    user_agent_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
                    connection.sendall(user_agent_response.encode())

                elif request_path[1] != '' and request_path[1] != "user-agent":
                    connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
                
                else:
                    connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

if __name__ == "__main__":
    main()
