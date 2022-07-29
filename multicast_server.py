import socket
import struct

MCAST_GRP = "224.1.1.1"
MCAST_PORT = 5004
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)
sock.bind(("", MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

#ID = int(input("Digite o ID do server: "))
TIME_TO_WAIT_ID = 4
TIME_TO_WAIT = 0.5

print('solicitando uma ID...')

#solicita uma nova id
try:
    
    sock.sendto(str.encode('RID'), (MCAST_GRP, MCAST_PORT))

    while True:

        sock.settimeout(TIME_TO_WAIT_ID)
        response = sock.recv(4096).decode()

        if response.__contains__('RID'):
            continue

        #verifica se uma id foi recebida
        if response.__contains__('NID'):
            ID = eval(response.split(':')[1])
            MAIOR_ID = ID
            break

except:
    #caso nenhuma id seja recebida, supõe-se que nenhum outro servidor esteja ativo
    print('Nenhuma resposta obtida.')
    ID = 1
    MAIOR_ID = 1


print('ID definida: {}'.format(ID))


while(True):
    try:
        sock.settimeout(None)
        request = sock.recv(4096).decode()

        if request.__contains__('response'):
            continue

        #requisição de id recebida
        if request.__contains__('RID'):
            print('Requisição por ID recebida...')
            try:
                #esperando resposta de outros servidores
                sock.settimeout(((ID * TIME_TO_WAIT_ID) / MAIOR_ID) - (TIME_TO_WAIT_ID/MAIOR_ID))
                while True:
                    response = sock.recv(4096).decode()

                    #atualizando ID máxima
                    if(response.__contains__('NID')):
                        MAIOR_ID = eval(response.split(':')[1])
                        print('Maior ID setada para: {}'.format(MAIOR_ID))
                        break

            except:
                #enviando resposta com o incremento da maior id
                print('Enviando ID {} como resposta...'.format(MAIOR_ID + 1))
                sock.sendto(str.encode('NID:{}'.format(MAIOR_ID + 1)), (MCAST_GRP, MCAST_PORT))
            
            continue
        
        #atualizando maior id, caso um NID seja recebido
        if request.__contains__('NID'):
            MAIOR_ID = eval(request.split(':')[1])
            continue


        if ID > 1:
            sock.settimeout(ID * TIME_TO_WAIT)
            try:
                response = sock.recv(4096).decode()
                continue
            except:
                print('O servidor com ID menor não respondeu no tempo estabelecido.')

        

        print("Recebido:{} ".format(request))
        response = "response:{}".format(eval(request))
        sock.sendto(str.encode(response), (MCAST_GRP, MCAST_PORT))
        print("Enviado: {}".format(response.split(":")[1]))


    except KeyboardInterrupt:
        print('Encerrando Programa.')
        exit()