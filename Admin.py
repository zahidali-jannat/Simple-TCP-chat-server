# Check whether kick request is sent by admin or not 
import threading
lock=threading.Lock()
def is_admin(requester, admin_client):
    return requester==admin_client

def kick_user(target_name , requester , client_socket , admin_client , lock , broadcast):
    if not is_admin(requester ,admin_client):
        try:
            requester.send("You are not admin".encode('ascii'))
        except:
            pass
        return
        
    with lock:
        for client , name in list(client_socket.items()):
            if name==target_name:
                try:

                    client.send("You were kicked by the server!".encode('ascii'))
                except:
                    pass    
                client.close()
                 
                del client_socket[client]

                broadcast(f"{target_name} was kicked".encode('ascii'))
                print(f"{target_name} kicked successfully")
                return 
        print("User not found")