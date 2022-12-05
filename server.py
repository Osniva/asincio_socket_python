import socket
import sys
import os
from select import select


to_monitor = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost',2001))
server.listen(2)


def acpt_conn(server):
    cl_sock, addr = server.accept()
    print('connection from', addr)
    if len(to_monitor) == 3:
        return 0
    to_monitor.append(cl_sock)

    print(len(to_monitor))
    
def send_file(socks):
    print (socks == to_monitor[1])
    print (socks == to_monitor[2])
    if socks == to_monitor[1]:
        print ('user 1 send messege for user 2')
        to_monitor[2].sendall(to_monitor[1].recv(4096))
    elif socks == to_monitor[2]:
        print ('user 2 send messege for user 1')
        to_monitor[1].sendall(to_monitor[2].recv(4096))
                
def event_loop():
    while True:

        ready_read, _, _ = select(to_monitor, [], [])

        for sock in ready_read:
            print(sock)
            if sock is server:
                acpt_conn(sock)
            elif len(to_monitor) == 3:
                send_file(sock)


if __name__ == '__main__':
    to_monitor.append(server)
    print(to_monitor)
    event_loop()
