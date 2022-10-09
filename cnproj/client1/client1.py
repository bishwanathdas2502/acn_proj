from ast import For
import socket
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
CLIENT_DATA_PATH = "client_data"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd == "GET_FILES":
            print(f"GET_FILE {client}")
            send_data = ""
            files = os.listdir(CLIENT_DATA_PATH)
            if len(files) != 0:
                send_data += "YES@"
                send_data += "\n".join(f for f in files)
                client.send(send_data.encode(FORMAT))
            else:
                client.send("NO@no files".encode(FORMAT))
        

        msg = input("> ")
        command = msg.split(" ")
        command = command[0]
        if(command == "LIST"):
            client.send(f'{command}@'.encode(FORMAT))
            listFile = client.recv(SIZE).decode(FORMAT)
            print(listFile)
        
        elif command == "REQUEST":
            client.send(f'{command}@{filename}'.encode(FORMAT))
            receive = client.recv(SIZE).decode('utf-8')
            res,filename,text = receive.split('@')
            if res == "NO":
                print('FILE not present')
            else:
                filepath = os.path.join(CLIENT_DATA_PATH, filename)
                with open(filepath,"w") as f:
                    f.write(text)
                
                log = "OK@file downloaded successfully"
                client.send(log.endcode(FORMAT))
    client.close()

if __name__ == "__main__":
    main() 