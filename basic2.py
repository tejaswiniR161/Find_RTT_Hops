import socket
import time
import matplotlib.pyplot as plt

maximumHops=30
port=33434
timeOut=30
serverDomain="google.com"

#question expects maximum length of the response to be 1500 and the payload to be 1472 and UDP header to be 8 bytes
responseLength=1500

#message data to be sent as asked in the question
data="measurement for class project. questions to student txr177@case.edu or professor mxr136@case.edu"

#payload=str(data+'a'*(1472-len(data))).encode('ascii')
payload = bytes(data + 'a'*(1472 - len(data)))

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

        sender.sendto(payload,(serverIP,port))
        data,currentAddress=receiver.recvfrom(responseLength)
        print("received data ",data)
        print("received address ",currentAddress)
    except socket.error:
        print("Something went wrong! ",socket.error)
    finally:
        sender.close()
        receiver.close()
    return(currentAddress[0])

def generateScatterPlot():
    x=[1,2,3]
    y=[1,2,3]
    labels=["tej","asw","ini"]
    for i in range(len(x)):
        plt.plot(x[i], y[i], 'bo')
        plt.text(x[i] * (1 + 0.01), y[i] * (1 + 0.01) , labels[i], fontsize=12)

    plt.xlim((0, 30))
    plt.ylim((0, 30))
    plt.show()

generateScatterPlot()
#numberOfHops(serverIP)