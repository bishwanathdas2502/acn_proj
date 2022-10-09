from email import message
from http import server
import threading
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 8000

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(('10.44.1.100',PORT))
server.listen()

clients = list()
names = list()


def broadcast(message):
    for client in clients:
        client.send(message)


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f'{name} left'.encode('utf-8'))
            names.remove(name)
            break

def receive():
    while True:
        print('Listening...')
        client,address = server.accept()
        print(f'connetion established with {str(address)}')
        client.send('name?'.encode('utf-8'))
        name = client.recv(1024)
        names.append(name)
        clients.append(client)
        print(f'{name} joined'.encode('utf-8'))
        broadcast(f'{name} is present'.encode('utf-8'))
        client.send('you are now connected'.encode('utf-8'))
        thread = threading.Thread(target=handle_client,args=(client,))
        thread.start()



if __name__ == "__main__":
    receive()