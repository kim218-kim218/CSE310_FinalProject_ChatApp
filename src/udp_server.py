import socket

HOST = '127.0.0.1'
PORT = 65433

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

clients = set()

print(f"🔵 UDP Server listening on {HOST}:{PORT}")

while True:
    msg, addr = server.recvfrom(1024)
    if addr not in clients:
        clients.add(addr)
        print(f"❗️ {addr} joined.")
    print(f"✉️ {addr}: {msg.decode('utf-8')}")
    
    # broadcast to all clients
    for client in clients:
        if client != addr:
            server.sendto(msg, client)
