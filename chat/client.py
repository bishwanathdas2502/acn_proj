from email import message
import threading
import socket

name = input('nickname')
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(('10.44.1.100',8000))


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if(message == "name?"):
                client.send(name.encode('utf-8'))
            else:
                print(message)
        except:
            print('Errior')


def client_send():
    while True:
        message = f'{name} : {input("")}'
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
