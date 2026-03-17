import socket
import threading

## Store all client fd in a list
all_clients = []
lock = threading.Lock()

def broadcast(message,sender_socket=None):
    """ Broadcast function broadcast messages to all clients """
    with lock:
        for client in all_clients:
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except Exception as err:
                    client.close()
                    if client in all_clients:
                        all_clients.remove(client)

def handle_client(client_conn,client_addr):
    """ Handle Client Conversation """
    print(f"Client Connected from [{client_addr}]")

    try:
        with client_conn:
            ## Ask User Name via send()
            client_conn.send(b"Enter Your Name: ")

            ## Recv Username from Client
            username = client_conn.recv(1024).decode().strip()

            if not username:
                return

            greet_message = f"{username} has Joined the chat!"

            ## Broadcast the message to all
            broadcast(greet_message,client_conn)

            while True:
                ## Recv Message from Client
                message = client_conn.recv(1024).decode()

                ## If client doesnt send any messages break it
                if not message:
                    break

                fmt_msg = f"{username}: {message}"

                ## Broadcast the Message to all the clients   
                broadcast(fmt_msg,client_conn)

    except ConnectionResetError:
        print(f"[DISCONNECT] {client_addr} forcibly closed the connection.")

    except Exception as err:
        print(f"[ERROR] Unexpected error with {client_addr}: {err}")

    finally:    
        with lock:
            if client_conn in all_clients:
                all_clients.remove(client_conn)

        client_conn.close()
            
        ## Disconnected message
        if 'username' in locals() and username:
            disconn_msg = f"{username} has Left the Chat!"
            broadcast(message=disconn_msg,sender_socket=client_conn)

def start_server():
    """ Start a Socket TCP Server"""
    # Initialize a Socket
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    host = ''
    port = 9999

    ## Bind the socket with ip and port
    server.bind((host,port))

    ## Listen for the connection
    server.listen(5)
    print(f"Server is Listenting at {host}:{port}.....")

    while True:
        ## Accept the connection
        sockfd,addr = server.accept()

        ## Add a current connection to the list
        with lock:
            all_clients.append(sockfd)

        thread = threading.Thread(target=handle_client,args=(sockfd,addr))
        thread.daemon = True
        thread.start()

        print(f"[Active Connections] : {len(all_clients)}")


if __name__ == '__main__':
    start_server()
