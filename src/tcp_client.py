import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# 닉네임 입력해서 서버에 먼저 전송
nickname = input("Enter your nickname: ")
client.sendall(nickname.encode('utf-8'))

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            print(f"{msg}") 
        except:
            print("🔴 Connection closed.")
            client.close()
            break


def send():
    while True:
        msg = input("")
        client.sendall(msg.encode('utf-8'))


# 쓰레드 2개로 동시에 송신/수신
threading.Thread(target=receive).start()
threading.Thread(target=send).start()
