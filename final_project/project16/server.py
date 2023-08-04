import socket
import secrets
from gmssl import sm2
def receive_P1(server):
    data, addr = server.recvfrom(1024)
    data = data.decode()
    index1 = data.index(',')
    P1 = (int(data[:index1]), int(data[index1 + 1:]))
    return P1, addr

def d_and_P(P1):
    """
    :param P1: d1^-1 * G
    :return: d2, P
    """
    d = secrets.randbelow(N)
    P = EC_sub(EC_multi(inv(d, N), P1), G)
    return d, P


def recv_T1_and_comp_T2(d2, server):
    data, addr = server.recvfrom(1024)
    data = data.decode()
    index1 = data.index(',')
    T1 = (int(data[:index1]), int(data[index1 + 1:]))
    T2 = EC_multi(inv(d2, N), T1)
    data = str(T2[0]) + ',' + str(T2[1])
    server.sendto(data.encode(), addr)

def interact():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('', 13800))
    while 1:  
        P1, addr = receive_P1(server)
        d2, P = d_and_P(P1)
        msg = "hahaha"
        print("Client需要恢复的明文消息为:", msg)
        ciphertext = SM2_enc(msg, P)
        data = str(ciphertext)
        server.sendto(data.encode(), addr)
        recv_T1_and_comp_T2(d2, server)
        print("-----------------------------------------------------------------")
    server.close()

N=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
if __name__ == '__main__':
    print("-----------------------------------------------------------------")
    print("                           Server端                              ")
    print("-----------------------------------------------------------------")
    interact()
