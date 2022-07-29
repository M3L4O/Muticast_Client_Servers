import socket
import struct

name = "sender"
MCAST_GRP = "224.1.1.1"
MCAST_PORT = 5004
# 2-hop restriction in network
ttl = 2
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
sock.bind(("", MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

expr = input("Digite uma expressão: ")
sock.sendto(str.encode(expr), (MCAST_GRP, MCAST_PORT))
print("Enviado: {}".format(expr))

sock.settimeout(10) #setando tempo máximo de espera
data = sock.recv(4096).decode()

while data.split(":")[0] != "response":
    print(data)
    data = sock.recv(4096).decode()
print("Recebido: {}".format(data.split(":")[1]))
