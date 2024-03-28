import socket, threading

server_ip = '127.0.0.1'
server_port = 999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = {}

server.bind((server_ip,server_port))

server.listen()
print("Waiting for connections\n")

def redirectMessages(client_socket):
    while(True):
        try:
            message = str(client_socket.recv(1024).decode())
            received_message = message.split(":")
            print(received_message)

            if(len(received_message) == 3):
                sender = received_message[0]
                receiver = received_message[1]
                message = sender + ":" + received_message[2]

                if(receiver in clients.keys()):
                    for client_name in clients.keys():
                        if(client_name == receiver):
                            receiver_socket = clients.get(client_name)
                            receiver_socket.send(message.encode())
                            break
                
                else:
                    print("Receiver does not exist")

            elif(len(received_message) == 4):
                sender = received_message[0]
                receiver = received_message[1]
                file_name = received_message[2]
                contents = received_message[3]

                message = sender + ":" + file_name + ":" + contents
                
                if(receiver in clients.keys()):
                    for client_name in clients.keys():
                        if(client_name == receiver):
                            receiver_socket = clients.get(client_name)
                            receiver_socket.send(message.encode())
                            break
                
                else:
                    print("Receiver does not exist")
                                
            elif(len(received_message) == 5):
                sender = received_message[0]
                receiver = received_message[1]
                file_name = received_message[2]
                contents = received_message[3]
                message = sender + ":" + file_name + ":" + contents + ":" + received_message[4]

                if(receiver in clients.keys()):
                    for client_name in clients.keys():
                        if(client_name == receiver):
                            receiver_socket = clients.get(client_name)
                            receiver_socket.send(message.encode())
                            break
                
                else:
                    print("Receiver does not exist")

            else:
                print("Invalid message format\nmessage:", message,"\nreceived message:",received_message)

        except ConnectionResetError as c:
            print(c)

            for name, socket in clients.items():
                if(client_socket == socket):
                    clients.pop(socket)
                    break
            
            print(clients.keys())
        
        except WindowsError as windows_error:
            print(windows_error)

            for name, socket in clients.items():
                if(client_socket == socket):
                    clients.pop(socket)
                    break
            
            print(clients.keys())


# def receiveMessages(client_socket):
#     while(True):
#         print("redirect messaging")
#         message = str(client_socket.recv(1024).decode())
#         print(message)

#         if(message.startswith("DEVELOPER") and "DEVELOPER" in clients.keys()):
#             sock = clients.get("DEVELOPER")
#             sock.send(1024).encode()

#         elif(message.startswith("MANAGER") and "MANAGER" in clients.keys()):
#             sock = clients.get("MANAGER")
#             sock.send(1024).encode()
        
#         elif(message.startswith("TESTER") and "TESTER" in clients.keys("TESTER")):
#             sock = clients.get("TESTER")
#             sock.send(1024).encode()

#         else:
#             print("The client you want to contact is offline")
        

while(True):
    client_socket, client_address = server.accept()
    print(client_address," is connected")
    client_name = client_socket.recv(1024).decode()
    print(client_name)
    clients.update({client_name : client_socket})
    print(clients.keys())
    client_socket.send("Connected to server successfully".encode())

    thread = threading.Thread(target=redirectMessages, args=(client_socket,))
    thread.start()