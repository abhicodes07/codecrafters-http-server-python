# Uncomment this to pass the first stage
import socket
import threading
import sys

def handle_requests(connection, address):
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

            print(f"Requested path: {request_path}")
            # print(f"Requeste path reversed: {reversed(request_path)}")
            print(f"request_data: {request_data}")
            # check_UserAgent = request_path[1] # user-agent

            if len(request_path) >= 3 and request_path[1] == "echo":
                content = request_path[2]
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
                connection.sendall(response.encode())

            elif request_path[1] != '' and request_path[1] == "user-agent":
                raw_agent = request_data[4].split("\r\n") # mango/grape-grape\r\n\r\n
                user_agent = raw_agent[0] # mango/grape-grape 

                user_agent_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
                connection.sendall(user_agent_response.encode())

            elif request_path[1] != '' and request_path[1] != "user-agent" and request_path[1] != "files":
                connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

            elif request_path[1] != '' and request_path[1] == "files":
                directory = sys.argv[2]
                filename = request_path[-1]
                print(directory, filename)
                with open(f"{directory}/{filename}","r") as f:
                    body = f.read()
                file_response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}"
                connection.sendall(file_response.encode())

            else:
                connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")



def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    with socket.create_server(("localhost", 4221), reuse_port=True) as server_socket:
    # server_socket.accept() # wait for client
        server_socket.listen()
        while True:
            connection, address = server_socket.accept()
            threading.Thread(target=handle_requests, args=(connection, address)).start()   
      
if __name__ == "__main__":
    main()
