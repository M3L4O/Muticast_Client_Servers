import socket
import struct
from time import sleep

MCAST_GRP = "224.1.1.1"
MCAST_PORT = 5004
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)
sock.bind(("", MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

ID = int(input("Digite o ID do server: "))
TIME_TO_WAIT = 2

while(True):
    try:
        sock.settimeout(None)
        request = sock.recv(4096).decode()

        if request.__contains__('response'):
            continue

        if ID > 1:
            sock.settimeout(ID * TIME_TO_WAIT)
            try:
                response = sock.recv(4096).decode()
                continue
            except:
                print('main server response timeout, sending response...')

        print("Recebido:{} ".format(request))
        response = "response:{}".format(eval(request))
        sock.sendto(str.encode(response), (MCAST_GRP, MCAST_PORT))
        print("Enviado: {}".format(response.split(":")[1]))


    except KeyboardInterrupt:
        print('Encerrando Programa.')