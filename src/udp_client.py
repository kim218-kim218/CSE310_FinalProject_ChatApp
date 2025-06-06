import socket
import threading

HOST = '127.0.0.1'
PORT = 65433

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

nickname = input("Enter your nickname: ")

def receive():
    while True:
        try:
            msg, _ = client.recvfrom(1024)
            print(f"{msg.decode('utf-8')}")
        except:
            break

def send():
    while True:
        msg = input()
        full_msg = f"{nickname:<5}: {msg}"
        client.sendto(full_msg.encode('utf-8'), (HOST, PORT))

# UDP는 연결 없음 → 아무 곳에서 그냥 sendto() 가능
# UDP는 connection이 없음 → 클라이언트가 먼저 sendto() 호출해서 "데이터를 보내기 전까지" 서버는 클라이언트가 존재하는지 모름.
# sendto()해야 server쪽에서 joined라고 뜸. 
# 서버가 클라이언트 addr 보고 관리

# clinet가 disconnect했는지 server에서는 알 수 없음
# why? -> connection이 없어서
# client가 꺼지거나 종료해도 server입장에서는 그냥 더이상 패킷이 안 온다는 것밖에 모름. 

# 실시간 스트리밍, 게임에서 자주 사용 -> 약간의 데이터가 빠져도 인경 안 쓰는 상황에서.

# How to improve? -> client가 종료하기 전에 특수 메시지를 전송해서 server쪽에서는 그 특수메시지를 보고 client제거 가능.

threading.Thread(target=receive).start()
threading.Thread(target=send).start()
