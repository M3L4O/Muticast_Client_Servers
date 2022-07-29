import socket
import struct

MCAST_GRP = "224.1.1.1"
MCAST_PORT = 5004
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)
sock.bind(("", MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

ID = int(input("Digite o ID do server: "))
TIME_TO_WAIT = 2
request = sock.recv(4096).decode()
while request.split(":")[0] == "response":
    request = sock.recv(4096).decode

if ID > 1:
    sock.settimeout(ID * TIME_TO_WAIT)
    try:
        request = sock.recv(4096).decode()
    except:
        print('Erro')

print("Recebido:{} ".format(request))
response = "response:{}".format(eval(request))
sock.sendto(str.encode(response), (MCAST_GRP, MCAST_PORT))
print("Enviado: {}".format(response.split(":")[1]))
