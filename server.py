import socket
import threading
import queue


messages = queue.Queue()
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))


def receive():
    while True:
        try:
            message, address = server.recvfrom(1024)
            messages.put((message, address))
        except socket.error as e:
            print("Error: " + e.strerror)
            break


def broadcast():
    while True:
        while not messages.empty():
            message, address = messages.get()
            print(message.decode())
            if address not in clients:
                clients.append(address)
            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG:"):
                        name = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} joined!".encode(), client)
                    else:
                        server.sendto(message, client)
                except socket.error:
                    clients.remove(client)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
