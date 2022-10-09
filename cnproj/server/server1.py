from http import client
import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

clients = list()

def handle_client(conn, addr):

    clients.append((conn,addr))
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))
    print(len(clients))
    
    
    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        if cmd == "LIST":
            print("here")
            str = ""
            for client in clients:
                con = client[0]
                if con != conn:
                    try:
                        con.send("GET_FILES@".encode(FORMAT))
                        r_msg = con.recv(SIZE).decode(FORMAT)
                        r_cmd,r_name = r_msg.split("@")
                        if r_cmd == "YES":
                            str += r_name
                    except:
                        continue
            print(str)
            conn.send(f'FILES_LIST@{str}'.encode(FORMAT))

                

        
    
    conn.close()

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()