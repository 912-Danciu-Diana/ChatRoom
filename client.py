import socket
import threading
#import random


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.bind(("localhost", 8888))
#clientSocket.bind(("localhost", random.randint(8000, 9000)))
name = input("Nickname: ")


def receive():
    while True:
        try:
            _message, _ = clientSocket.recvfrom(1024)
            print(_message.decode())
        except socket.error as e:
            print("Error: " + e.strerror)


t = threading.Thread(target=receive)
t.start()

clientSocket.sendto(f"SIGNUP_TAG:{name}".encode(), ("localhost", 9999))

while True:
    message = input("")
    if message == "!q":
        exit()
    else:
        clientSocket.sendto(f"{name}: {message}".encode(), ("localhost", 9999))
