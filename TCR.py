import threading
import socket
from Admin import kick_user , is_admin
host='127.0.0.1'                                # Local host 
port=55555

# Teri behen koh namannn

server=socket.socket(socket.AF_INET , socket.SOCK_STREAM)
  
server.bind((host , port ))
server.listen()                                  # server starts listening for new clients 
lock = threading.Lock()
admin_name="ZAHID"
admin_client=None                                                 # First here i am going to use two empty list here when ever if new will join the server we will
                                              # put that client in clients list and their nick name in nicknames list 

clients=[]
nicknames=[]

client_socket={}
                                                  #Broad cast function is the most simple function which sends  messages  to those clients 
                                                  # which are connected to the server right now 
def broadcast(message):
    with lock: 
        for client in list(client_socket):
            try:
                client.send(message)
            except:
                print("Client disconnected unexpectedly")

                client_socket.pop(client, None)  
                try:
                    client.close()
                except:
                    pass

                                                  # Next part handle client connection with server 
def handle(client):
    while True:
        try:
            message = client.recv(1024).decode()

            if not message:
                break
            if client==admin_client: # he is admin 
                if message.startswith("/kick"):
                    parts=message.split()
                    if len(parts)>1:
                        target=parts[1]
                        kick_user(target , client , client_socket , admin_client , lock , broadcast)
                        # broadcast(f"Admin has kicked the {target}".encode())   
                    
                else:
                    broadcast(f" Admin : {message} ".encode('ascii'))  
            else:
                if message.startswith("/kick"):
                    client.send("You cannot kick any one".encode('ascii'))
                else:
                 
                    broadcast(f"{client_socket[client]}: {message}".encode('ascii'))            

        except:
            nickname=None
            with lock:
                if client in client_socket:
                    nickname = client_socket[client]
                    del client_socket[client]

            if nickname:
                broadcast(f"{nickname} left the chat".encode())

            client.close()
            break         


def receive():
    while True:
        client , address=server.accept()           # Accept client all the time get there address and client name 
        global admin_client
        print(f"Connected with {str(address)}")
        
        client.send('NICK_NAME'.encode('ascii'))   # Particular client koh bheja hua message  
        nickname=client.recv(1024).decode('ascii') # Receive nick name from the client 
        # nicknames.append(nickname)               # Decoded form mai naame liye daala andr direct 
        # clients.append(client)
        client_socket[client]=nickname
        if(nickname==admin_name):
            if admin_client is None:

                admin_client=client
                broadcast(f" {nickname} Admin Joined the chat !!!!! ".encode('ascii'))
            else:
                 client.send("Admin already added".encode('ascii'))
                 client.close()
                 continue 
        else:
            
            print(f"Nickaname of the client is {client_socket[client]}")
            broadcast(f"{client_socket[client]} joined the chat ".encode('ascii'))
            client.send("Connected to the server".encode('ascii'))

        thread=threading.Thread(target=handle, args=(client, ))
        thread.start()

# def kick_user(username):
#     with lock:
#         for client , name in list(client_socket.items()):
#             if name==username:
#                 client.send("You were kicked by the server!".encode('ascii'))
#                 client.close()
#                 if client in clients:
#                     index = clients.index(client)
#                     clients.remove(client)
#                     nicknames.pop(index)

#                 del client_socket[client]

#                 broadcast(f"{username} was kicked".encode('ascii'))
#                 print(f"{username} kicked successfully")
#                 return 
#         print("User not found")    
# def server_commands(): 
#     while True:
#         cmd=input()
#         if cmd.startswith("kick"):
#             parts=cmd.split()

#             if len(parts) > 1:
#                 username=parts[1]
#                 kick_user(username)  
  
# threading.Thread(target=server_commands, daemon=True).start() 
                      
print("Server is listening to client......... ")

receive()        