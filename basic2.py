import socket
import time

maximumHops=30
port=33444
serverDomain="google.com"
serverIP=socket.gethostbyname(serverDomain)
print("address of the server = ",serverIP)

def numberOfHops(serverIP):
    for i in range(1,maximumHops):
        print("pinging the server with current ttl = ",i)
        currentAddress=pingServer(serverIP,i,port)
        if currentAddress.find(serverIP)!=-1:
            print("reached the server already!")
            exit(0)

def pingServer(serverIP,currentTimeOut,port):
    #sender=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
    #receiver=socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)

    sender=socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    sender.setsockopt(socket.SOL_IP, socket.IP_TTL,currentTimeOut)

    receiver=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
    receiver.bind(("",port))

    try:

        sender.sendto(b'',(serverIP,port))
        data,currentAddress=receiver.recvfrom(1024)
        print("received data ",data)
        print("received address ",currentAddress)
    except socket.error:
        print("Something went wrong! ",socket.error)
    finally:
        sender.close()
        receiver.close()
    return(currentAddress[0])

numberOfHops(serverIP)