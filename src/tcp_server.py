import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = {}

def broadcast(message, sender_client):
    for client in clients:
        if client != sender_client:
            client.sendall(message)

def handle_client(client):
    try:
        # 처음에 닉네임 받기
        nickname = client.recv(1024).decode('utf-8')
        nicknames[client] = nickname
        print(f"V {nickname} connected.")

        # 다른 클라이언트에게 접속 알림 보내기
        join_msg = f"🟢 {nickname} joined the chat.".encode('utf-8')
        broadcast(join_msg, client)

        while True:
            msg = client.recv(1024)
            if not msg:
                break
            # 닉네임 붙여서 broadcast
            message_with_nick = f"{nicknames[client]}: {msg.decode('utf-8')}".encode('utf-8')
            broadcast(message_with_nick, client)
    except:
        pass
    finally:
        # 연결 종료 처리
        print(f"X {nicknames[client]} disconnected.")
        clients.remove(client)
        # 나간 메시지도 broadcast
        leave_msg = f"🔴 {nicknames[client]} left the chat.".encode('utf-8')
        broadcast(leave_msg, client)
        del nicknames[client]
        client.close()

print(f"🔵 Server listening on {HOST}:{PORT}")
while True:
    client, addr = server.accept()
    clients.append(client)
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()
