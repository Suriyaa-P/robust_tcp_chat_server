import socket
import threading
from time import sleep

def receive_messages(client_socket):
    """Continuously receive and display messages from server"""
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message:
                print("\n[DISCONNECTED] Lost connection to server")
                break
            
            print(f"\n{message}")
            print("You: ", end='', flush=True)
            
        except:
            break

def send_messages(client_socket):
    """Get user input and send to server"""
    
    while True:
        message = input("You: ")
        
        if message.lower() == 'quit':
            client_socket.send(b"Good Bye Guys! I will catch you later.")
            sleep(0.3)
            break
        
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            print("\n[ERROR] Could not send message")
            break

def start_client():
    # Connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    HOST = '127.0.0.1'
    PORT = 9999
    
    try:
        client_socket.connect((HOST, PORT))
        print(f"[CONNECTED] Connected to {HOST}:{PORT}")
    except:
        print("[ERROR] Could not connect to server")
        return
    
    # Get username
    prompt = client_socket.recv(1024).decode('utf-8')
    username = input(prompt)
    client_socket.send(username.encode('utf-8'))
    
    # Start receive thread
    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,)
    )
    receive_thread.daemon = True
    receive_thread.start()
    
    # Main thread handles sending
    send_messages(client_socket)
    
    # Cleanup
    client_socket.close()
    print("[DISCONNECTED] Goodbye!")


if __name__ == "__main__":
    start_client()